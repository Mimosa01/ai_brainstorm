from uuid import uuid4

def id_generate () -> str:
  return str(uuid4())[:6]