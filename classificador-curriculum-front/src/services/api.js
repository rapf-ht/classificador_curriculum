const API_URL = import.meta.env.VITE_API_URL

export async function analisarCurriculo(arquivo, vaga) {
  const formData = new FormData();
  formData.append('curriculo', arquivo);
  formData.append('vaga', vaga);

  const response = await fetch(`${API_URL}/analisar`, {
    method: 'POST',
    body: formData,
    // NÃO definir Content-Type manualmente — o navegador gera
    // automaticamente o boundary correto do multipart/form-data
  });

  if (!response.ok) {
    const erro = await response.json().catch(() => null);
    throw new Error(erro?.detail || `Erro ${response.status} ao analisar currículo.`);
  }

  return response.json();
}