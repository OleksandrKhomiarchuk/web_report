document.addEventListener("DOMContentLoaded", () => {
    loadHomepage();
});

function loadHomepage() {
    document.getElementById("content").innerHTML = `
        <h1>Report of Monaco 2018 Racing 🏁 🏎 </h1>
              <ul>
                <p>This web application is designed to generate a report on the Formula 1 race held in Monaco in 2018.</p>
                <p>The app allows you to view a list of riders, a full race report, and also view information about a specific rider.</p>
                <p>You can also sort lists in ascending and descending order.</p>
              </ul>
    `;
}

function loadDrivers() {
    fetch('/api/v1/report/drivers/?format=json')
        .then(response => response.json())
        .then(data => {
            let html = `<h1>Drivers List</h1>
                               <table class="table table-bordered">
                                    <thead>
                                        <tr>
                                            <th>Name</th>
                                            <th>Abbreviation</th>
                                        </tr>
                                    </thead>
                               <tbody>`;
            data.forEach(driver => {
                html += `<tr>
                            <td><a href="#" onclick="loadDriver('${driver.abbreviation}')">${driver.name}</a></td>
                            <td><a href="#" onclick="loadDriver('${driver.abbreviation}')">${driver.abbreviation}</a></td>
                         </tr>`;
            });
            html += "</tbody></table>";
            document.getElementById("content").innerHTML = html;
        });
}

function loadDriver(driverId) {
    fetch(`/api/v1/report/drivers/?format=json&driver_id=${driverId}`)
        .then(response => response.json())
        .then(driver => {
            if (driver.error) {
                document.getElementById("content").innerHTML = `<h1>Driver not found</h1>`;
            } else {
                document.getElementById("content").innerHTML = `
                    <h1>Driver Info</h1>
                    <p><strong>Name:</strong> ${driver.name}</p>
                    <p><strong>Abbreviation:</strong> ${driver.abbreviation}</p>
                    <p><strong>Date:</strong> ${driver.date}</p>
                    <p><strong>Team:</strong> ${driver.team}</p>
                    <p><strong>Lap Time:</strong> ${driver.lap_time}</p>
                    <p><strong>Position:</strong> ${driver.position}</p>
                `;
            }
        });
}

let sortOrder = "asc";

function loadReport() {
    fetch('/api/v1/report/?format=json')
        .then(response => response.json())
        .then(data => {
            function parseLapTime(lapTime) {
                const [minutes, seconds, milliseconds] = lapTime.split(/[:.]/).map(Number);
                return (minutes * 60 * 1000) + (seconds * 1000) + milliseconds;
            }

            data.sort((a, b) => {
                const timeA = parseLapTime(a.lap_time);
                const timeB = parseLapTime(b.lap_time);
                return sortOrder === "asc" ? timeA - timeB : timeB - timeA;
            });

            let html = `<h1>Race Report</h1>
                        <table class="table table-bordered">
                            <thead>
                                <tr>
                                    <th>Position</th>
                                    <th>Date</th>
                                    <th>Name</th>
                                    <th>Team</th>
                                    <th>
                                        <button class="btn btn-primary mb-2" style="padding: 0.25rem 0.5rem; 
                                            font-size: 0.800rem;
                                            " onclick="toggleSort()">Lap Time (${sortOrder.toUpperCase()})
                                        </button>
                                    </th>
                                </tr>
                            </thead>
                            <tbody>`;

            data.forEach((driver, index) => {
                html += `<tr>
                            <td>${driver.position}</td>
                            <td>${driver.date}</td>
                            <td><a href="#" onclick="loadDriver('${driver.abbreviation}')">${driver.name}</a></td>
                            <td>${driver.team}</td>
                            <td>${driver.lap_time}</td>
                         </tr>`;
            });

            html += "</tbody></table>";
            document.getElementById("content").innerHTML = html;
        });
}

function toggleSort() {
    sortOrder = sortOrder === "asc" ? "desc" : "asc";
    loadReport();
}

function handleSearch(event) {
    event.preventDefault();
    const driverId = document.getElementById("driver_id").value;
    loadDriver(driverId);
}
