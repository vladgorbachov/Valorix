document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM полностью загружен");

    const themeToggle = document.getElementById("themeToggle");
    const chartDiv = document.getElementById("chart");
    let darkTheme = localStorage.getItem("darkTheme") === "true";

    const updateTheme = () => {
        document.body.classList.toggle("dark-theme", darkTheme);
        localStorage.setItem("darkTheme", darkTheme);
    };

    themeToggle.addEventListener("click", () => {
        darkTheme = !darkTheme;
        updateTheme();
    });

    updateTheme();

    const loadChart = async (interval) => {
        const response = await fetch(`/api/v1/candlestick?interval=${interval}`);
        const { data } = await response.json();

        const plotData = [
            {
                x: data.map(item => new Date(item.time)),
                open: data.map(item => item.open),
                high: data.map(item => item.high),
                low: data.map(item => item.low),
                close: data.map(item => item.close),
                type: "candlestick",
            },
        ];

        Plotly.newPlot(chartDiv, plotData, {
            title: "Crypto Market",
            xaxis: { title: "Time" },
            yaxis: { title: "Price" },
        });
    };

    // Изначальная загрузка
    loadChart("1h");

    document.querySelectorAll("button[data-interval]").forEach(button => {
        button.addEventListener("click", () => {
            const interval = button.getAttribute("data-interval");
            loadChart(interval);
        });
    });
});
