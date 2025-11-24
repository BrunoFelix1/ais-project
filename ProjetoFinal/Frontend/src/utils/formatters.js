/**
 * Formata valor monetário para BRL
 * @param {number} value - Valor a ser formatado
 * @returns {string} Valor formatado
 */
export const formatCurrency = (value) => {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(value || 0);
};

/**
 * Formata número com separadores de milhar
 * @param {number} value - Número a ser formatado
 * @returns {string} Número formatado
 */
export const formatNumber = (value) => {
  return new Intl.NumberFormat("pt-BR").format(value || 0);
};

/**
 * Trunca texto com reticências
 * @param {string} text - Texto a ser truncado
 * @param {number} maxLength - Tamanho máximo
 * @returns {string} Texto truncado
 */
export const truncateText = (text, maxLength = 50) => {
  if (!text || text.length <= maxLength) return text;
  return text.substring(0, maxLength) + "...";
};

/**
 * Capitaliza primeira letra de cada palavra
 * @param {string} text - Texto a ser capitalizado
 * @returns {string} Texto capitalizado
 */
export const capitalizeWords = (text) => {
  if (!text) return "";
  return text
    .toLowerCase()
    .split(" ")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
};
