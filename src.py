import pandas as pd
import random
from flask import Flask, render_template_string, request

# Predefined list of districts with latitude and longitude
districts_info = [
    {"Area": "Ariyalur", "Latitude": 11.1385, "Longitude": 79.0756},
    {"Area": "Chengalpattu", "Latitude": 12.697, "Longitude": 79.9828},
    {"Area": "Chennai", "Latitude": 13.0827, "Longitude": 80.2707},
    {"Area": "Coimbatore", "Latitude": 11.0168, "Longitude": 76.9558},
    {"Area": "Cuddalore", "Latitude": 11.748, "Longitude": 79.7714},
    {"Area": "Dharmapuri", "Latitude": 12.1357, "Longitude": 78.1612},
    {"Area": "Dindigul", "Latitude": 10.362, "Longitude": 77.9705},
    {"Area": "Erode", "Latitude": 11.341, "Longitude": 77.7172},
    {"Area": "Kallakurichi", "Latitude": 11.7386, "Longitude": 78.9604},
    {"Area": "Kancheepuram", "Latitude": 12.8342, "Longitude": 79.7036},
    {"Area": "Karur", "Latitude": 10.9601, "Longitude": 78.0766},
    {"Area": "Krishnagiri", "Latitude": 12.5186, "Longitude": 78.2133},
    {"Area": "Madurai", "Latitude": 9.9252, "Longitude": 78.1198},
    {"Area": "Mayiladuthurai", "Latitude": 11.1035, "Longitude": 79.655},
    {"Area": "Nagapattinam", "Latitude": 10.7656, "Longitude": 79.8425},
    {"Area": "Kanyakumari", "Latitude": 8.0883, "Longitude": 77.5385},
    {"Area": "Namakkal", "Latitude": 11.2186, "Longitude": 78.1676},
    {"Area": "Perambalur", "Latitude": 11.2333, "Longitude": 78.8833},
    {"Area": "Pudukottai", "Latitude": 10.3797, "Longitude": 78.82},
    {"Area": "Ramanathapuram", "Latitude": 9.3708, "Longitude": 78.8307},
    {"Area": "Ranipet", "Latitude": 12.9337, "Longitude": 79.3339},
    {"Area": "Salem", "Latitude": 11.6643, "Longitude": 78.146},
    {"Area": "Sivagangai", "Latitude": 9.8478, "Longitude": 78.488},
    {"Area": "Tenkasi", "Latitude": 8.9587, "Longitude": 77.3152},
    {"Area": "Thanjavur", "Latitude": 10.7867, "Longitude": 79.1391},
    {"Area": "Theni", "Latitude": 10.0104, "Longitude": 77.4777},
    {"Area": "Thiruvallur", "Latitude": 13.1431, "Longitude": 79.9085},
    {"Area": "Thiruvarur", "Latitude": 10.7672, "Longitude": 79.6366},
    {"Area": "Tuticorin", "Latitude": 8.7642, "Longitude": 78.1348},
    {"Area": "Tiruchirappalli", "Latitude": 10.7905, "Longitude": 78.7047},
    {"Area": "Thirunelveli", "Latitude": 8.7139, "Longitude": 77.7567},
    {"Area": "Tirupathur", "Latitude": 12.495, "Longitude": 78.5653},
    {"Area": "Tiruppur", "Latitude": 11.1085, "Longitude": 77.3411},
    {"Area": "Tiruvannamalai", "Latitude": 12.2253, "Longitude": 79.0747},
    {"Area": "The Nilgiris", "Latitude": 11.4143, "Longitude": 76.695},
    {"Area": "Vellore", "Latitude": 12.9165, "Longitude": 79.1325},
    {"Area": "Viluppuram", "Latitude": 11.9401, "Longitude": 79.4977},
    {"Area": "Virudhunagar", "Latitude": 9.5741, "Longitude": 77.9624},
]

# Generate synthetic dataset
data = []
for district in districts_info:
    traffic_density = random.randint(100, 5000)  # vehicles/km²
    traffic_condition = random.choice(["Low", "Moderate", "High", "Congested"])
    electrical_consumption = [round(random.uniform(50, 500), 2) for _ in range(7)]  # Weekly kWh/day
    avg_temperature = [round(random.uniform(20, 40), 1) for _ in range(7)]  # Weekly °C
    weather_condition = random.choice(["Sunny", "Rainy", "Cloudy", "Stormy", "Clear"])

    # Add data to the list
    data.append({
        "Area": district["Area"],
        "Latitude": district["Latitude"],
        "Longitude": district["Longitude"],
        "Traffic Density (vehicles/km²)": traffic_density,
        "Traffic Condition": traffic_condition,
        "Electrical Consumption (kWh/day)": electrical_consumption,
        "Average Temperature (°C)": avg_temperature,
        "Weather Condition": weather_condition
    })

# Create a DataFrame from the generated data
df = pd.DataFrame(data)

# Flask application
app = Flask(__name__)

# Template for the web page
template = """ 

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart City Planner</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- jQuery -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <!-- Leaflet for Map -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f4f6f9;
        }
        header {
            text-align: center;
            background: #2c3e50;
            color: #fff;
            padding: 20px 0;
            margin-bottom: 20px;
        }
        main {
            max-width: 900px;
            margin: auto;
            background: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        }
        .loader {
            display: none;
            border: 8px solid #f3f3f3;
            border-radius: 50%;
            border-top: 8px solid #3498db;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .card-body canvas {
            margin-top: 20px;
        }
        #map {
            height: 400px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <header>
        <h1>Smart City Planner</h1>
    </header>
    <main>
        <!-- Input Form -->
        <form method="POST" id="districtForm">
            <div class="mb-3">
                <label for="district" class="form-label">Enter District:</label>
                <input type="text" class="form-control" id="district" name="district" placeholder="Enter district name">
            </div>
            <button type="submit" class="btn btn-primary w-100">Visualize</button>
        </form>
        
        <div class="loader"></div>

        {% if error %}
        <div class="alert alert-danger mt-3">{{ error }}</div> 
        {% endif %}

        {% if data %}
        <!-- Dashboard Content -->
        <div id="dashboard">
            <h2>{{ data['Area'] }} - Insights</h2>
            
            <div class="row mt-3">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">Traffic Condition</div>
                        <div class="card-body">
                            <p>Traffic Density: {{ data['Traffic Density (vehicles/km²)'] }} vehicles/km²</p>
                            <p>Condition: {{ data['Traffic Condition'] }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">Weather</div>
                        <div class="card-body">
                            <p>Weather: {{ data['Weather Condition'] }}</p>
                            <p>Average Temperature: {{ data['Average Temperature (°C)'][0] }}°C</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Temperature Graph -->
            <div class="card mt-3">
                <div class="card-header">Weekly Temperature Trend</div>
                <div class="card-body">
                    <canvas id="tempChart"></canvas>
                </div>
            </div>

            <!-- Electricity Consumption Graph -->
            <!-- Electricity Consumption Analysis -->
            <div class="card mt-3">
                <div class="card-header bg-success text-white">
                    Electricity Usage Analysis (Weekly)
                </div>
                <div class="card-body">
                    <!-- Bar Chart for Daily Consumption -->
                    <h5>Daily Consumption (kWh)</h5>
                    <canvas id="elecBarChart"></canvas>
            
                    <!-- Pie Chart for Consumption by Categories -->
                    <h5 class="mt-4">Consumption by Category</h5>
                    <canvas id="elecCategoryChart"></canvas>
            
                    <!-- Line Chart for Cumulative Consumption -->
                    <h5 class="mt-4">Cumulative Consumption (kWh)</h5>
                    <canvas id="elecCumulativeChart"></canvas>
                </div>
            </div>
            
            
            <!-- Traffic Charts -->
            <div class="card mt-3">
                <div class="card-header bg-warning text-dark">
                    Traffic Density Analysis
                </div>
                <div class="card-body">
                    <!-- Pie Chart for Vehicle Breakdown -->
                    <h5>Vehicle Type Breakdown</h5>
                    <canvas id="trafficPieChart"></canvas>

                    <!-- Traffic by Hour -->
                    <h5 class="mt-4">Hourly Traffic Density</h5>
                    <canvas id="trafficLineChart"></canvas>
                </div>
            </div>

            <!-- Map -->
            <div class="card mt-3">
                <div class="card-header">Location Map</div>
                <div class="card-body">
                    <div id="map"></div>
                </div>
            </div>
        </div>
        {% endif %}
    </main>

    <script>
        $(document).ready(function () {
            // Show loader when submitting form
            $("#districtForm").submit(function (event) {
                $(".loader").show();
            });

            {% if data %}
            // Temperature Chart
            var tempCtx = document.getElementById('tempChart').getContext('2d');
            new Chart(tempCtx, {
                type: 'line',
                data: {
                    labels: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
                    datasets: [{
                        label: 'Avg Temperature (°C)',
                        data: {{ data['Average Temperature (°C)'] }},
                        fill: false,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        tension: 0.1
                    }]
                }
            });

            // Electricity Chart
                        // Electricity Bar Chart (Daily Consumption)
            var elecBarCtx = document.getElementById('elecBarChart').getContext('2d');
            new Chart(elecBarCtx, {
                type: 'bar',
                data: {
                    labels: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
                    datasets: [{
                        label: 'Daily Electricity Consumption (kWh)',
                        data: {{ data['Electrical Consumption (kWh/day)'] }},
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { display: true }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Electricity (kWh)'
                            }
                        }
                    }
                }
            });

            // Electricity Pie Chart (Consumption by Category)
            var elecCategoryCtx = document.getElementById('elecCategoryChart').getContext('2d');
            new Chart(elecCategoryCtx, {
                type: 'pie',
                data: {
                    labels: ['Residential', 'Commercial', 'Industrial'],
                    datasets: [{
                        label: 'Electricity Consumption by Category',
                        data: [40, 35, 25], // Simulated percentages
                        backgroundColor: ['#ff9999', '#66b3ff', '#99ff99']
                    }]
                }
            });

            // Electricity Cumulative Line Chart
            var elecCumulativeCtx = document.getElementById('elecCumulativeChart').getContext('2d');
            var dailyData = {{ data['Electrical Consumption (kWh/day)'] }};
            var cumulativeData = dailyData.reduce((acc, value, index) => {
                acc.push((acc[index - 1] || 0) + value);
                return acc;
            }, []);
            new Chart(elecCumulativeCtx, {
                type: 'line',
                data: {
                    labels: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
                    datasets: [{
                        label: 'Cumulative Electricity Consumption (kWh)',
                        data: cumulativeData,
                        fill: false,
                        borderColor: 'rgba(153, 102, 255, 1)',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { display: true }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Cumulative Electricity (kWh)'
                            }
                        }
                    }
                }
            });

            // Traffic Pie Chart
            var trafficPieCtx = document.getElementById('trafficPieChart').getContext('2d');
            new Chart(trafficPieCtx, {
                type: 'pie',
                data: {
                    labels: ['Cars', 'Bikes', 'Buses', 'Trucks'],
                    datasets: [{
                        data: [60, 20, 10, 10],
                        backgroundColor: ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
                    }]
                }
            });

            // Traffic Line Chart
            var trafficLineCtx = document.getElementById('trafficLineChart').getContext('2d');
            new Chart(trafficLineCtx, {
                type: 'line',
                data: {
                    labels: ['6 AM', '9 AM', '12 PM', '3 PM', '6 PM', '9 PM', '12 AM'],
                    datasets: [{
                        label: 'Hourly Traffic Density',
                        data: [1200, 2000, 3500, 4000, 3000, 2500, 1000],
                        borderColor: '#ffcc00',
                        tension: 0.4
                    }]
                }
            });

            // Map
            var map = L.map('map').setView([{{ data['Latitude'] }}, {{ data['Longitude'] }}], 12);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
            L.marker([{{ data['Latitude'] }}, {{ data['Longitude'] }}]).addTo(map)
                .bindPopup('<b>{{ data['Area'] }}</b>').openPopup();
            {% endif %}
        });
    </script>
</body>
</html>



 """

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        district_name = request.form.get("district")
        if not district_name:
            error = "Please enter a district name."
            return render_template_string(template, error=error, data=None)

        data = df[df["Area"].str.contains(district_name, case=False)]
        if not data.empty:
            return render_template_string(template, data=data.iloc[0].to_dict())
        else:
            error = "District not found!"
            return render_template_string(template, error=error, data=None)

    return render_template_string(template, error=None, data=None)

if __name__ == "__main__":
    app.run(debug=True)
