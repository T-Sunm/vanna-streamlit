import re
import requests
from vanna.base import VannaBase


class CustomGroq(VannaBase):
    """
    Lớp tùy chỉnh để kết nối Vanna với Groq Cloud API.
    """

    def __init__(self, config=None):
        if config is None or "api_key" not in config:
            raise ValueError("Config phải chứa 'api_key' cho Groq.")

        self.api_key = config["api_key"]
        self.model = config.get("model", "llama3-70b-8192")  # Đặt model mặc định
        self.temperature = config.get("temperature", 0.7)
        self.base_url = "https://api.groq.com/openai/v1"

    def system_message(self, message: str) -> dict:
        return {"role": "system", "content": message}

    def user_message(self, message: str) -> dict:
        return {"role": "user", "content": message}

    def assistant_message(self, message: str) -> dict:
        return {"role": "assistant", "content": message}

    def submit_prompt(self, prompt, **kwargs) -> str:
        url = f"{self.base_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        data = {
            "model": self.model,
            "messages": prompt,
            "temperature": self.temperature,
            "stream": False,
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            # Thêm dòng này để báo lỗi nếu request thất bại (ví dụ: 401, 404, 500)
            response.raise_for_status()

            response_dict = response.json()
            return response_dict["choices"][0]["message"]["content"]

        except requests.exceptions.RequestException as e:
            # Xử lý lỗi một cách rõ ràng
            print(f"Lỗi khi gọi API Groq: {e}")
            if response is not None:
                print(f"Response body: {response.text}")
            return "SELECT 'API_CALL_ERROR' as error;"  # Trả về một SQL lỗi để không làm sập chương trình

    def extract_sql_query(self, text: str) -> str:
        # Giữ nguyên logic trích xuất SQL từ class Vllm
        pattern = re.compile(r"select.*?(?:;|```|$)", re.IGNORECASE | re.DOTALL)
        match = pattern.search(text)
        if match:
            return match.group(0).replace("```", "").strip()
        return text

    def generate_sql(self, question: str, **kwargs) -> str:

        prompt = self.get_prompt_context(question=question, **kwargs)

        # Gửi prompt đến LLM thông qua hàm submit_prompt đã viết
        llm_response = self.submit_prompt(prompt)

        # Xử lý và trích xuất câu lệnh SQL từ kết quả trả về
        sql = llm_response.replace("\\_", "_").replace("\\", "")
        return self.extract_sql_query(sql)
