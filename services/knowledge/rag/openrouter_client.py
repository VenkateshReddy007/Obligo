import os
from openai import OpenAI

from services.api.config import settings

SYSTEM_PROMPT = (
    "You are a compliance expert for Indian SMBs. Always cite which regulation you are referencing. "
    "Never make up due dates or rates — use only the provided context. If uncertain, say so explicitly."
)


class OpenRouterComplianceClient:
    def __init__(self) -> None:
        self.api_key = (
            settings.openrouter_api_key
            or os.getenv("OPENROUTER_API_KEY", "")
        )
        self.base_url = settings.openrouter_base_url
        self.model = settings.openrouter_model

        # Initialize OpenAI-compatible client
        # If API key is not yet set, use a dummy token to prevent init-time crashes
        # and guard runtime calls with a helpful configuration message.
        client_key = self.api_key.strip() if self.api_key else "placeholder-key"
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=client_key,
        )

    def is_configured(self) -> bool:
        return bool(self.api_key and self.api_key.strip() and self.api_key.strip() != "placeholder-key")

    def generate_compliance_response(self, system_prompt: str, user_query: str, context: str) -> dict:
        if not self.is_configured():
            return {
                "response": "OpenRouter API key is not configured. Please add your OPENROUTER_API_KEY to the .env file.",
                "model_used": self.model,
                "tokens_used": 0,
            }

        prompt = f"Context:\n{context}\n\nUser Query:\n{user_query}"

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            max_tokens=1024,
        )

        text = response.choices[0].message.content or ""
        tokens = response.usage.total_tokens if response.usage else len(prompt.split()) + len(text.split())
        return {"response": text, "model_used": self.model, "tokens_used": tokens}

    def generate_plain_language_card(self, regulation_changes: list, business_profile: dict) -> str:
        if not self.is_configured():
            return "A regulation update may affect your obligations. Please review pending tasks."

        business_name = business_profile.get("name", "the business")
        change_text = "; ".join([str(c) for c in regulation_changes])
        prompt = f"Create a concise plain-language compliance card for {business_name}. Changes: {change_text}"

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
        )
        return response.choices[0].message.content or ""

    def generate_audit_packet_summary(self, audit_entries: list) -> str:
        if not self.is_configured():
            return "Audit log summary unavailable: OpenRouter API key not configured."

        prompt = f"Summarize these audit entries for an auditor:\n{audit_entries[:30]}"

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
        )
        return response.choices[0].message.content or ""


# Alias for compatibility
ComplianceClient = OpenRouterComplianceClient
