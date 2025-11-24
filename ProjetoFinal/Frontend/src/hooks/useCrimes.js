import { useState, useEffect, useCallback } from "react";
import { crimeService } from "../services/crimeService";

export const useCrimes = () => {
  const [aggregations, setAggregations] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchAggregations = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await crimeService.getAggregations();
      setAggregations(data.data || []);
    } catch (err) {
      setError(err.message || "Erro ao buscar dados");
      console.error("Erro ao buscar agregações:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchStats = useCallback(async () => {
    try {
      setError(null);
      const data = await crimeService.getStats();
      setStats(data.data || null);
    } catch (err) {
      setError(err.message || "Erro ao buscar estatísticas");
      console.error("Erro ao buscar estatísticas:", err);
    }
  }, []);

  const uploadCsv = async (file) => {
    try {
      setLoading(true);
      setError(null);
      const result = await crimeService.uploadCsv(file);
      await fetchAggregations();
      await fetchStats();
      return result;
    } catch (err) {
      setError(err.message || "Erro ao fazer upload");
      console.error("Erro ao fazer upload:", err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const clearData = async () => {
    try {
      setLoading(true);
      setError(null);
      await crimeService.clearData();
      setAggregations([]);
      setStats(null);
    } catch (err) {
      setError(err.message || "Erro ao limpar dados");
      console.error("Erro ao limpar dados:", err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAggregations();
    fetchStats();
  }, [fetchAggregations, fetchStats]);

  return {
    aggregations,
    stats,
    loading,
    error,
    uploadCsv,
    clearData,
    refresh: () => {
      fetchAggregations();
      fetchStats();
    },
  };
};
