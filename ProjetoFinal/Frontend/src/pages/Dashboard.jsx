import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { crimeService } from "../services/crimeService";

import "./Dashboard.css";
const fallbackCenter = [-8.0476, -34.8761];

const Dashboard = () => {
  const [aggregations, setAggregations] = useState([]);
  const [stats, setStats] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedBairro, setSelectedBairro] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadFeedback, setUploadFeedback] = useState({
    type: "",
    message: "",
  });
  const fileInputRef = useRef(null);

  const fetchDashboardData = useCallback(async () => {
    try {
      setIsRefreshing(true);
      setErrorMessage("");

      const [aggregationsResponse, statsResponse] = await Promise.all([
        crimeService.getAggregations(),
        crimeService.getStats(),
      ]);

      const aggregationsData = aggregationsResponse?.data || [];

      setAggregations(aggregationsData);
      setSelectedBairro((previous) => {
        if (
          previous &&
          aggregationsData.some((item) => item.bairro === previous.bairro)
        ) {
          return (
            aggregationsData.find((item) => item.bairro === previous.bairro) ||
            null
          );
        }
        return aggregationsData[0] || null;
      });

      setStats(statsResponse?.data || null);
    } catch (error) {
      console.error("Erro ao carregar dashboard", error);
      setErrorMessage(
        "Não foi possível carregar os dados. Tente novamente em instantes."
      );
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  }, []);

  useEffect(() => {
    fetchDashboardData();
  }, [fetchDashboardData]);

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];
    setSelectedFile(file || null);
    setUploadFeedback({ type: "", message: "" });
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadFeedback({
        type: "error",
        message: "Selecione um arquivo CSV para enviar.",
      });
      return;
    }

    try {
      setUploading(true);
      setUploadFeedback({ type: "", message: "" });
      await crimeService.uploadCsv(selectedFile);
      setUploadFeedback({
        type: "success",
        message: "Arquivo enviado com sucesso! Processando novos dados...",
      });
      setSelectedFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
      await fetchDashboardData();
    } catch (uploadError) {
      console.error("Erro ao enviar CSV", uploadError);
      setUploadFeedback({
        type: "error",
        message: "Falha no upload. Verifique o arquivo e tente novamente.",
      });
    } finally {
      setUploading(false);
    }
  };

  const formatNumber = (value) => {
    const safeValue = Number.isFinite(value) ? value : 0;
    return safeValue.toLocaleString("pt-BR");
  };

  const formatCurrency = (value) => {
    const safeValue = Number.isFinite(value) ? value : 0;
    return safeValue.toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL",
      maximumFractionDigits: 0,
    });
  };

  const filteredAggregations = useMemo(() => {
    const normalizedTerm = searchTerm.trim().toLowerCase();
    const list = [...aggregations];
    if (normalizedTerm) {
      return list
        .filter((item) =>
          (item?.bairro || "").toLowerCase().includes(normalizedTerm)
        )
        .sort((a, b) => (b.total_crimes || 0) - (a.total_crimes || 0));
    }
    return list.sort((a, b) => (b.total_crimes || 0) - (a.total_crimes || 0));
  }, [aggregations, searchTerm]);

  const topBairros = useMemo(() => {
    return [...aggregations]
      .sort((a, b) => (b.total_crimes || 0) - (a.total_crimes || 0))
      .slice(0, 4);
  }, [aggregations]);

  const mapMarkers = useMemo(() => {
    return aggregations.filter(
      (item) =>
        Number.isFinite(item?.latitude_media) &&
        Number.isFinite(item?.longitude_media)
    );
  }, [aggregations]);

  const maxTotalCrimes = useMemo(() => {
    if (!aggregations.length) {
      return 0;
    }
    return aggregations.reduce(
      (max, item) => Math.max(max, item?.total_crimes || 0),
      0
    );
  }, [aggregations]);

  const mapCenter = useMemo(() => {
    if (
      Number.isFinite(selectedBairro?.latitude_media) &&
      Number.isFinite(selectedBairro?.longitude_media)
    ) {
      return [selectedBairro.latitude_media, selectedBairro.longitude_media];
    }

    if (mapMarkers.length) {
      const avgLat =
        mapMarkers.reduce((sum, item) => sum + item.latitude_media, 0) /
        mapMarkers.length;
      const avgLng =
        mapMarkers.reduce((sum, item) => sum + item.longitude_media, 0) /
        mapMarkers.length;
      return [avgLat, avgLng];
    }

    return fallbackCenter;
  }, [mapMarkers, selectedBairro]);

  const getMarkerRadius = (totalCrimes) => {
    if (!maxTotalCrimes) {
      return 8;
    }
    return Math.max(8, (totalCrimes / maxTotalCrimes) * 26);
  };

  const getMarkerColor = (totalCrimes) => {
    if (!maxTotalCrimes) {
      return "#2563eb";
    }
    const percentage = totalCrimes / maxTotalCrimes;
    if (percentage >= 0.75) return "#dc2626";
    if (percentage >= 0.5) return "#f97316";
    if (percentage >= 0.25) return "#eab308";
    return "#22c55e";
  };

  const hasData = aggregations.length > 0;

  return (
    <div className="crime-dashboard">
      <div className="crime-dashboard__layout">
        <header className="crime-dashboard__header">
          <div>
            <h1 className="crime-dashboard__title">Monitoramento de Crimes</h1>
            <p className="crime-dashboard__subtitle">
              Acompanhe os índices de criminalidade das suas bases de dados.
            </p>
          </div>
          <button
            type="button"
            className="crime-dashboard__button primary"
            onClick={fetchDashboardData}
            disabled={isRefreshing}
          >
            {isRefreshing ? "Atualizando..." : "Atualizar dados"}
          </button>
        </header>
        {errorMessage && (
          <div className="crime-dashboard__alert">{errorMessage}</div>
        )}

        <section className="upload-card">
          <div className="upload-card__info">
            <h3>Enviar novos registros</h3>
            <p>
              Atualize as informações de criminalidade com novas bases de dados.
            </p>
          </div>
          <div className="upload-card__actions">
            <label
              className={`upload-card__file ${selectedFile ? "has-file" : ""}`}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".csv"
                onChange={handleFileChange}
              />
              <span>
                {selectedFile
                  ? selectedFile.name
                  : "Selecione um arquivo CSV atualizado"}
              </span>
            </label>
            <button
              type="button"
              className="crime-dashboard__button primary upload-card__button"
              onClick={handleUpload}
              disabled={!selectedFile || uploading}
            >
              {uploading ? "Enviando..." : "Enviar arquivo"}
            </button>
          </div>
          {uploadFeedback.message && (
            <p
              className={`upload-card__feedback ${
                uploadFeedback.type === "error" ? "error" : "success"
              }`}
            >
              {uploadFeedback.message}
            </p>
          )}
        </section>

        <section className="crime-dashboard__stats">
          <article className="stats-card">
            <p className="stats-card__label">Crimes registrados</p>
            <p
              className={`stats-card__value ${
                isLoading ? "loading-pulse" : ""
              }`}
            >
              {stats ? formatNumber(stats.total_crimes) : "--"}
            </p>
            {stats?.total_crimes && stats?.total_prejuizo ? (
              <div className="stats-card__secondary">
                <span>Prejuízo médio</span>
                <strong>
                  {formatCurrency(
                    stats.total_prejuizo / Math.max(stats.total_crimes, 1)
                  )}
                </strong>
              </div>
            ) : null}
          </article>
          <article className="stats-card">
            <p className="stats-card__label">Impacto financeiro</p>
            <p
              className={`stats-card__value ${
                isLoading ? "loading-pulse" : ""
              }`}
            >
              {stats ? formatCurrency(stats.total_prejuizo) : "--"}
            </p>
            {stats?.total_prejuizo && stats?.total_bairros ? (
              <div className="stats-card__secondary">
                <span>Média por bairro</span>
                <strong>
                  {formatCurrency(
                    stats.total_prejuizo / Math.max(stats.total_bairros, 1)
                  )}
                </strong>
              </div>
            ) : null}
          </article>
          <article className="stats-card">
            <p className="stats-card__label">Bairros monitorados</p>
            <p
              className={`stats-card__value ${
                isLoading ? "loading-pulse" : ""
              }`}
            >
              {stats ? formatNumber(stats.total_bairros) : "--"}
            </p>
            {stats?.total_crimes && stats?.total_bairros ? (
              <div className="stats-card__secondary">
                <span>Crimes médios/bairro</span>
                <strong>
                  {formatNumber(
                    Math.round(
                      stats.total_crimes / Math.max(stats.total_bairros, 1)
                    )
                  )}
                </strong>
              </div>
            ) : null}
          </article>
          <article className="stats-card">
            <p className="stats-card__label">Maior incidência</p>
            <p
              className={`stats-card__value ${
                isLoading ? "loading-pulse" : ""
              }`}
            >
              {stats?.bairro_mais_crimes?.bairro || "--"}
            </p>
            {stats?.bairro_mais_crimes ? (
              <div className="stats-card__secondary">
                <span>Total de ocorrências</span>
                <strong>
                  {formatNumber(stats.bairro_mais_crimes.total_crimes || 0)}
                </strong>
              </div>
            ) : null}
          </article>
        </section>

        <section className="crime-dashboard__grid">
          <article className="card">
            <div className="map-panel__header">
              <div>
                <p className="map-panel__subtitle">Mapa inteligente</p>
                <h2 className="map-panel__title">Distribuição de crimes</h2>
              </div>
            </div>
            {hasData ? (
              <>
                <MapContainer
                  key={`${mapCenter[0]}-${mapCenter[1]}`}
                  center={mapCenter}
                  zoom={12}
                  scrollWheelZoom
                  className="map-panel__map"
                >
                  <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution="&copy; OpenStreetMap"
                  />
                  {mapMarkers.map((item) => (
                    <CircleMarker
                      key={item.bairro}
                      center={[item.latitude_media, item.longitude_media]}
                      radius={getMarkerRadius(item.total_crimes || 0)}
                      pathOptions={{
                        color: getMarkerColor(item.total_crimes || 0),
                        fillColor: getMarkerColor(item.total_crimes || 0),
                        fillOpacity: 0.45,
                        weight: 2,
                      }}
                      eventHandlers={{
                        click: () => setSelectedBairro(item),
                      }}
                    >
                      <Popup>
                        <strong>{item.bairro}</strong>
                        <br />
                        {formatNumber(item.total_crimes)} crimes
                        <br />
                        {formatCurrency(item.prejuizo_total)} em prejuízo
                      </Popup>
                    </CircleMarker>
                  ))}
                </MapContainer>
                <div className="map-panel__legend">
                  <span>
                    <span
                      className="map-panel__legend-dot"
                      style={{ background: "#22c55e" }}
                    />{" "}
                    Baixa incidência
                  </span>
                  <span>
                    <span
                      className="map-panel__legend-dot"
                      style={{ background: "#eab308" }}
                    />{" "}
                    Atenção
                  </span>
                  <span>
                    <span
                      className="map-panel__legend-dot"
                      style={{ background: "#f97316" }}
                    />{" "}
                    Criticidade
                  </span>
                  <span>
                    <span
                      className="map-panel__legend-dot"
                      style={{ background: "#dc2626" }}
                    />{" "}
                    Muito crítico
                  </span>
                </div>
              </>
            ) : (
              <div className="empty-state">
                Faça upload do CSV para visualizar o mapa de crimes.
              </div>
            )}
          </article>

          <article className="card">
            <div className="list-panel__header">
              <div>
                <p className="list-panel__subtitle">Prioridade de resposta</p>
                <h2 className="list-panel__title">Bairros monitorados</h2>
              </div>
            </div>

            <div className="list-panel__search">
              <input
                type="search"
                placeholder="Busque pelo nome do bairro"
                value={searchTerm}
                onChange={(event) => setSearchTerm(event.target.value)}
              />
            </div>

            {topBairros.length > 0 && (
              <div className="list-panel__chips">
                {topBairros.map((bairro, index) => (
                  <span
                    key={`${bairro.bairro || "bairro"}-${index}`}
                    className="list-panel__chip"
                  >
                    {bairro.bairro || "Bairro não informado"}
                  </span>
                ))}
              </div>
            )}

            {hasData ? (
              <div className="bairro-list">
                {filteredAggregations.map((item, index) => (
                  <button
                    type="button"
                    key={`${item.bairro || "bairro"}-${index}`}
                    className={`bairro-row ${
                      selectedBairro?.bairro === item.bairro
                        ? "bairro-row--active"
                        : ""
                    }`}
                    onClick={() => setSelectedBairro(item)}
                  >
                    <div className="bairro-row__info">
                      <h4>{item.bairro}</h4>
                      <p>{formatNumber(item.total_crimes)} crimes</p>
                    </div>
                    <div className="bairro-row__value">
                      {formatCurrency(item.prejuizo_total)}
                    </div>
                  </button>
                ))}
              </div>
            ) : (
              <div className="empty-state">Nenhuma informação disponível.</div>
            )}

            {selectedBairro && (
              <div className="selected-panel">
                <p className="selected-panel__title">{selectedBairro.bairro}</p>
                <div className="selected-panel__stat">
                  <span>Crimes registrados:</span>
                  <strong>{formatNumber(selectedBairro.total_crimes)}</strong>
                </div>
                <div className="selected-panel__stat">
                  <span>Prejuízo estimado:</span>
                  <strong>
                    {formatCurrency(selectedBairro.prejuizo_total)}
                  </strong>
                </div>
                <div className="selected-panel__stat">
                  <span>Coordenadas médias:</span>
                  <strong>
                    {Number.isFinite(selectedBairro.latitude_media) &&
                    Number.isFinite(selectedBairro.longitude_media)
                      ? `${selectedBairro.latitude_media.toFixed(
                          4
                        )}, ${selectedBairro.longitude_media.toFixed(4)}`
                      : "Não informado"}
                  </strong>
                </div>
              </div>
            )}
          </article>
        </section>
      </div>
    </div>
  );
};

export default Dashboard;
