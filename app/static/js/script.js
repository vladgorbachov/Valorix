// script.js
// This file is part of the client-side application for rendering candlestick charts and data panels.

document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM fully loaded");

    const themeToggle = document.getElementById("themeToggle");
    const chartDiv = document.getElementById("chart");
    const forexChartDiv = document.getElementById("forex-chart");
    const cryptoChartDiv = document.getElementById("crypto-chart");
    const indexChartDiv = document.getElementById("index-chart");

    let darkTheme = localStorage.getItem("darkTheme") === "true";

    const updateTheme = () => {
        document.body.classList.toggle("dark-theme", darkTheme);
        localStorage.setItem("darkTheme", darkTheme);

        const layoutUpdate = {
            paper_bgcolor: darkTheme ? "#000000" : "#ffffff",
            plot_bgcolor: darkTheme ? "#000000" : "#ffffff",
            font: { color: darkTheme ? "#ffffff" : "#000000" },
        };

        [chartDiv, forexChartDiv, cryptoChartDiv, indexChartDiv].forEach((div) => {
            if (div.data) {
                Plotly.relayout(div, layoutUpdate);
            }
        });
    };

    themeToggle.addEventListener("click", () => {
        darkTheme = !darkTheme;
        updateTheme();
    });

    updateTheme();

    const loadChartData = async (url, chartDiv, title, isCandlestick = false) => {
        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

            const data = await response.json();
            const chartData = Array.isArray(data) ? data : data.data;

            if (!chartData || chartData.length === 0) {
                chartDiv.innerHTML = `<p>No data available for ${title}</p>`;
                return;
            }

            let plotData;
            if (isCandlestick) {
                plotData = [
                    {
                        x: chartData.map(item => new Date(item.time)),
                        open: chartData.map(item => item.open),
                        high: chartData.map(item => item.high),
                        low: chartData.map(item => item.low),
                        close: chartData.map(item => item.close),
                        type: "candlestick",
                    },
                ];
            } else {
                plotData = [
                    {
                        x: chartData.map(item => item.name || item.symbol),
                        y: chartData.map(item => item.value || item.price),
                        type: "bar",
                        marker: {
                            color: darkTheme ? "#ffffff" : "#007bff",
                        },
                    },
                ];
            }

            const layout = {
                title,
                xaxis: { title: isCandlestick ? "Time" : "Assets" },
                yaxis: { title: "Value" },
                paper_bgcolor: darkTheme ? "#000000" : "#ffffff",
                plot_bgcolor: darkTheme ? "#000000" : "#ffffff",
                font: { color: darkTheme ? "#ffffff" : "#000000" },
            };

            Plotly.newPlot(chartDiv, plotData, layout);
        } catch (error) {
            console.error(`Error loading data for ${title}:`, error);
            chartDiv.innerHTML = `<p>Error loading data for ${title}</p>`;
        }
    };

    const updateDataPeriodically = () => {
        setInterval(() => loadChartData("/api/v1/crypto", cryptoChartDiv, "Cryptocurrencies"), 10000);
        setInterval(() => loadChartData("/api/v1/forex", forexChartDiv, "Forex Market"), 60000);
        setInterval(() => loadChartData("/api/v1/market", indexChartDiv, "Stock Indices"), 60000);
    };

    // Initialize the Bitcoin candlestick chart
    loadChartData("/api/v1/candlestick?interval=1h", chartDiv, "Bitcoin Candlestick", true);

    // Initialize other charts
    loadChartData("/api/v1/crypto", cryptoChartDiv, "Cryptocurrencies");
    loadChartData("/api/v1/forex", forexChartDiv, "Forex Market");
    loadChartData("/api/v1/market", indexChartDiv, "Stock Indices");

    // Start periodic updates
    updateDataPeriodically();
});
