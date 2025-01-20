document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM полностью загружен");

    const themeToggle = document.getElementById("themeToggle");
    const chartDiv = document.getElementById("chart");
    let darkTheme = localStorage.getItem("darkTheme") === "true";
    let isChartInitialized = false; // Флаг для проверки существования графика

    const updateTheme = () => {
        document.body.classList.toggle("dark-theme", darkTheme);
        localStorage.setItem("darkTheme", darkTheme);

        if (isChartInitialized) {
            // Обновление темы для уже существующего графика
            const layoutUpdate = {
                paper_bgcolor: darkTheme ? "#000000" : "#ffffff",
                plot_bgcolor: darkTheme ? "#000000" : "#ffffff",
                font: { color: darkTheme ? "#ffffff" : "#000000" },
                xaxis: { color: darkTheme ? "#ffffff" : "#000000" },
                yaxis: { color: darkTheme ? "#ffffff" : "#000000" },
            };
            Plotly.relayout(chartDiv, layoutUpdate);
        }
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

        const layout = {
            title: "Crypto Market",
            xaxis: { title: "Time", color: darkTheme ? "#ffffff" : "#000000" },
            yaxis: { title: "Price", color: darkTheme ? "#ffffff" : "#000000" },
            paper_bgcolor: darkTheme ? "#000000" : "#ffffff",
            plot_bgcolor: darkTheme ? "#000000" : "#ffffff",
            font: { color: darkTheme ? "#ffffff" : "#000000" },
        };

        // Создание или обновление графика
        if (!isChartInitialized) {
            Plotly.newPlot(chartDiv, plotData, layout);
            isChartInitialized = true; // Устанавливаем флаг после создания графика
        } else {
            Plotly.react(chartDiv, plotData, layout); // Обновляем данные и тему
        }
    };

    // Изначальная загрузка графика
    loadChart("1h");

    // Добавление событий для переключения интервалов
    document.querySelectorAll("button[data-interval]").forEach(button => {
        button.addEventListener("click", () => {
            const interval = button.getAttribute("data-interval");
            loadChart(interval);
        });
    });
});
