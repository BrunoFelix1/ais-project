import api from "./api";

export const crimeService = {
  /**
   * Faz upload de arquivo CSV
   * @param {File} file - Arquivo CSV a ser enviado
   * @returns {Promise} Resposta da API
   */
  uploadCsv: async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await api.post("/crimes/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  },

  /**
   * Busca agregações de crimes por bairro
   * @returns {Promise} Lista de agregações
   */
  getAggregations: async () => {
    const response = await api.get("/crimes/aggregations");
    return response.data;
  },

  /**
   * Busca agregação de um bairro específico
   * @param {string} bairro - Nome do bairro
   * @returns {Promise} Dados do bairro
   */
  getAggregationByBairro: async (bairro) => {
    const response = await api.get(`/crimes/aggregations/${bairro}`);
    return response.data;
  },

  /**
   * Busca estatísticas gerais
   * @returns {Promise} Estatísticas gerais
   */
  getStats: async () => {
    const response = await api.get("/crimes/stats");
    return response.data;
  },

  /**
   * Limpa todos os dados
   * @returns {Promise} Confirmação
   */
  clearData: async () => {
    const response = await api.delete("/crimes/clear");
    return response.data;
  },
};
