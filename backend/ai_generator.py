from typing import Optional, List, Dict
from openai import OpenAI


class AIGenerator:
    """Generates answers using OpenAI chat completions with course context."""

    SYSTEM_PROMPT = (
        "You are an AI assistant who answers questions about course materials. "
        "Use the provided course excerpts to craft concise, factual answers. "
        "If the context does not contain the answer, clearly state that the material is unavailable. "
        "When examples help, include short bullet points."
    )

    def __init__(self, api_key: str, model: str):
        self.model = model
        self.api_key = (api_key or "").strip()
        self.client: Optional[OpenAI] = None
        self._offline_reason: Optional[str] = None

        if self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
            except Exception as exc:
                # Record why the client failed so we can fall back gracefully.
                self._offline_reason = str(exc)
        else:
            self._offline_reason = "OpenAI API key not configured"

    def generate_response(
        self,
        query: str,
        conversation_history: Optional[str] = None,
        context: Optional[str] = None,
    ) -> str:
        """Create an answer, falling back to deterministic output if the model is unavailable."""
        if not self.client:
            return self._fallback_response(context)

        messages = self._build_messages(query, conversation_history, context)

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0,
                max_tokens=800,
            )
            return completion.choices[0].message.content.strip()
        except Exception as exc:
            return self._fallback_response(context, reason=str(exc))

    def _build_messages(
        self,
        query: str,
        conversation_history: Optional[str],
        context: Optional[str],
    ) -> List[Dict[str, str]]:
        """Compose the chat history sent to OpenAI."""
        messages: List[Dict[str, str]] = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
        ]

        if conversation_history:
            messages.append({
                "role": "user",
                "content": f"Conversation so far:\n{conversation_history}",
            })

        if context:
            messages.append({
                "role": "user",
                "content": f"Relevant course excerpts:\n{context}",
            })

        messages.append({"role": "user", "content": query})
        return messages

    def _fallback_response(self, context: Optional[str], reason: Optional[str] = None) -> str:
        """Return a deterministic answer when the OpenAI client cannot be used."""
        if reason:
            print(f"AI fallback activated: {reason}")

        if context:
            return (
                "The language model is offline, but here are the most relevant course excerpts:\n\n"
                f"{context}"
            )

        if self._offline_reason:
            return (
                "The assistant is temporarily offline. "
                "Set OPENAI_API_KEY and try again once the service is reachable."
            )

        return "The assistant is temporarily offline; try again shortly."
