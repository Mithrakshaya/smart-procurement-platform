import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [dashboardData, setDashboardData] = useState(null);
  const [centreData, setCentreData] = useState([]);
  const [alertsData, setAlertsData] = useState([]);

useEffect(() => {
  fetch("http://127.0.0.1:8000/dashboard/summary")
    .then((response) => response.json())
    .then((data) => {
      setDashboardData(data);
    })
    .catch((error) => {
      console.error("Error fetching dashboard data:", error);
    });

  fetch("http://127.0.0.1:8000/dashboard/centres")
    .then((response) => response.json())
    .then((data) => {
      setCentreData(data);
    })
    .catch((error) => {
      console.error("Error fetching centre data:", error);
    });
    fetch("http://127.0.0.1:8000/dashboard/alerts")
  .then((response) => response.json())
  .then((data) => {
    setAlertsData(data);
  })
  .catch((error) => {
    console.error("Error fetching alerts:", error);
  });
}, []);

  return (
    <div className="app">

      {/* Sidebar */}
      <aside className="sidebar">

        <div className="logo">
          🌾 GrainFlow
        </div>

        <nav>
          <div className="nav-item active">🏠 Dashboard</div>
          <div className="nav-item">📅 Appointments</div>
          <div className="nav-item">🎟️ Queue Management</div>
          <div className="nav-item">🌾 Procurement</div>
          <div className="nav-item">📊 Reports</div>
          <div className="nav-item">⚙️ Settings</div>
        </nav>

      </aside>


      {/* Main Content */}
      <main className="main-content">

        {/* Header */}
        <div className="header">
          <h1>Procurement Centre Dashboard</h1>
          <p>Monitor farmers, appointments and procurement activities</p>
        </div>


        {/* Statistics */}
<div className="stats">

  <div className="card">
    <h3>Today's Farmers</h3>
    <p>{dashboardData ? dashboardData.todays_farmers : "..."}</p>
  </div>

  <div className="card">
    <h3>Upcoming Appointments</h3>
    <p>{dashboardData ? dashboardData.upcoming_appointments : "..."}</p>
  </div>

  <div className="card">
    <h3>Current Queue</h3>
    <p>{dashboardData ? dashboardData.current_queue : "..."}</p>
  </div>

  <div className="card">
    <h3>Average Waiting Time</h3>
    <p>{dashboardData ? `${dashboardData.average_waiting_time} min` : "..."}</p>
  </div>

</div>


        {/* Appointments */}
        <div className="appointments">

          <h2>Today's Appointments</h2>

          <table>
            <thead>
              <tr>
                <th>Farmer</th>
                <th>Time</th>
                <th>Token</th>
                <th>Crop</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>

              <tr>
                <td>Ramesh Kumar</td>
                <td>09:30 AM</td>
                <td>#101</td>
                <td>Rice</td>
                <td>
                  <span className="status waiting">Waiting</span>
                </td>
              </tr>

              <tr>
                <td>Suresh Rao</td>
                <td>10:00 AM</td>
                <td>#102</td>
                <td>Wheat</td>
                <td>
                  <span className="status completed">Completed</span>
                </td>
              </tr>

              <tr>
                <td>Ravi Krishna</td>
                <td>10:30 AM</td>
                <td>#103</td>
                <td>Rice</td>
                <td>
                  <span className="status processing">Processing</span>
                </td>
              </tr>

              <tr>
                <td>Venkat Rao</td>
                <td>11:00 AM</td>
                <td>#104</td>
                <td>Maize</td>
                <td>
                  <span className="status waiting">Waiting</span>
                </td>
              </tr>

            </tbody>
          </table>

        </div>


        {/* Bottom Section */}
        <div className="bottom-section">

          {/* Centre Status */}
<div className="status-panel">

  <h2>🏢 Centre Status</h2>

  <div className="status-item">
    <span>Queue Status</span>
    <strong className="active-text">Active</strong>
  </div>

  <div className="status-item">
    <span>Available Counters</span>
    <strong>3 / 4</strong>
  </div>

  <div className="status-item">
    <span>Expected Arrivals</span>
    <strong>
      {dashboardData ? dashboardData.expected_arrivals : "..."}
    </strong>
  </div>

  <div className="status-item">
    <span>Congestion Level</span>
    <strong className="medium-text">
      {dashboardData ? dashboardData.congestion_level : "..."}
    </strong>
  </div>

</div>


          {/* Procurement Progress */}
<div className="progress-panel">

  <h2>🌾 Procurement Progress</h2>

  <div className="progress-info">
    <span>Daily Target</span>
    <strong>
      {dashboardData ? `${dashboardData.daily_target} Quintals` : "..."}
    </strong>
  </div>

  <div className="progress-info">
    <span>Procured</span>
    <strong>
      {dashboardData ? `${dashboardData.procured} Quintals` : "..."}
    </strong>
  </div>

  <div className="progress-bar">
    <div
      className="progress-fill"
      style={{
        width: dashboardData
          ? `${Math.round(
              (dashboardData.procured / dashboardData.daily_target) * 100
            )}%`
          : "0%",
      }}
    ></div>
  </div>

  <p className="progress-text">
    {dashboardData
      ? `${Math.round(
          (dashboardData.procured / dashboardData.daily_target) * 100
        )}% of today's target completed`
      : "..."}
  </p>

  <div className="progress-info">
    <span>Remaining</span>
    <strong>
      {dashboardData ? `${dashboardData.remaining} Quintals` : "..."}
    </strong>
  </div>

</div>

        </div>

        {/* Queue Management */}
<div className="queue-section">

  <h2>🎟️ Queue Management</h2>

  <div className="queue-summary">

    <div className="queue-card">
      <span>Current Token</span>
      <strong>#103</strong>
    </div>

    <div className="queue-card">
      <span>Now Processing</span>
      <strong>Ravi Krishna</strong>
    </div>

    <div className="queue-card">
      <span>Waiting Farmers</span>
      <strong>
        {dashboardData ? dashboardData.current_queue : "..."}
      </strong>
    </div>

    <div className="queue-card">
      <span>Estimated Wait</span>
      <strong>
        {dashboardData
          ? `${dashboardData.average_waiting_time} min`
          : "..."}
      </strong>
    </div>

  </div>

  <h3>Live Queue</h3>

  <table>
    <thead>
      <tr>
        <th>Token</th>
        <th>Farmer</th>
        <th>Crop</th>
        <th>Counter</th>
        <th>Status</th>
      </tr>
    </thead>

    <tbody>
      <tr>
        <td>#101</td>
        <td>Ramesh Kumar</td>
        <td>Rice</td>
        <td>Counter 1</td>
        <td><strong>Waiting</strong></td>
      </tr>

      <tr>
        <td>#102</td>
        <td>Suresh Rao</td>
        <td>Wheat</td>
        <td>Counter 3</td>
        <td><strong>Completed</strong></td>
      </tr>

      <tr>
        <td>#103</td>
        <td>Ravi Krishna</td>
        <td>Rice</td>
        <td>Counter 2</td>
        <td><strong>Processing</strong></td>
      </tr>

      <tr>
        <td>#104</td>
        <td>Venkat Rao</td>
        <td>Maize</td>
        <td>Counter 1</td>
        <td><strong>Waiting</strong></td>
      </tr>
    </tbody>
  </table>

</div>
{/* Congestion & AI Prediction */}
<div className="prediction-section">

  <h2>🚨 Congestion & AI Prediction</h2>

  <div className="prediction-grid">

    <div className="prediction-card">
      <span>Current Congestion</span>
      <strong className="medium-text">
        {dashboardData ? dashboardData.congestion_level : "..."}
      </strong>
      <p>Queue is manageable</p>
    </div>

    <div className="prediction-card">
      <span>Expected Arrivals</span>
      <strong>
        {dashboardData
          ? `${dashboardData.expected_arrivals} Farmers`
          : "..."}
      </strong>
      <p>Expected today</p>
    </div>

    <div className="prediction-card">
      <span>Predicted Waiting Time</span>
      <strong>
        {dashboardData
          ? `${dashboardData.average_waiting_time} min`
          : "..."}
      </strong>
      <p>Based on current queue</p>
    </div>

    <div className="prediction-card">
      <span>Peak Time</span>
      <strong>10 AM - 12 PM</strong>
      <p>High farmer arrivals expected</p>
    </div>

  </div>

  <div className="ai-recommendation">
    <h3>🤖 AI Recommendation</h3>
    <p>
      Consider opening an additional procurement counter during
      peak hours to reduce waiting time and congestion.
    </p>
  </div>

</div>

          
{/* Government / Admin Dashboard */}
<div className="admin-section">

  <h2>🏛️ Government / Admin Dashboard</h2>

  <p className="admin-subtitle">
    Monitor procurement centres, farmers, queues and overall performance
  </p>

  {/* Admin Statistics */}
  <div className="admin-stats">

    <div className="admin-card">
      <span>Total Centres</span>
      <strong>24</strong>
    </div>

    <div className="admin-card">
      <span>Total Farmers</span>
      <strong>2,450</strong>
    </div>

    <div className="admin-card">
      <span>Total Procurement</span>
      <strong>18,750 Q</strong>
    </div>

    <div className="admin-card">
      <span>Avg. Waiting Time</span>
      <strong>28 min</strong>
    </div>

  </div>

  {/* Centre-wise Performance */}
  <div className="centre-performance">

    <h3>📊 Centre-wise Performance</h3>

    <table>
      <thead>
        <tr>
          <th>Centre</th>
          <th>Farmers</th>
          <th>Queue</th>
          <th>Procurement</th>
          <th>Status</th>
        </tr>
      </thead>

     <tbody>
  {centreData.map((centre, index) => (
    <tr key={index}>
      <td>{centre.centre}</td>
      <td>{centre.farmers}</td>
      <td>{centre.queue}</td>
      <td>{centre.procurement} Q</td>
      <td>{centre.status}</td>
    </tr>
  ))}
</tbody>
    </table>

  </div>

{/* System Alerts */}
<div className="system-alerts">

  <h3>🚨 System Alerts</h3>

  {alertsData.map((alert, index) => (
    <div className="alert-item" key={index}>
      <strong>
        {alert.type === "warning" ? "⚠️" : "🤖"} {alert.title}
      </strong>

      <p>{alert.message}</p>
    </div>
  ))}

</div>

</div>
{/* Reports & Analytics */}
<div className="reports-section">

  <h2>📊 Reports & Analytics</h2>

  <p className="reports-subtitle">
    Analyse procurement, farmer visits and queue performance
  </p>

  <div className="report-grid">

    <div className="report-card">
      <span>Daily Procurement</span>
      <strong>
        {dashboardData ? `${dashboardData.procured} Q` : "..."}
      </strong>
      <p>
        {dashboardData
          ? `${Math.round(
              (dashboardData.procured / dashboardData.daily_target) * 100
            )}% of daily target`
          : "..."}
      </p>
    </div>

    <div className="report-card">
      <span>Farmer Visits</span>
      <strong>
        {dashboardData ? dashboardData.todays_farmers : "..."}
      </strong>
      <p>Farmers served today</p>
    </div>

    <div className="report-card">
      <span>Average Waiting Time</span>
      <strong>
        {dashboardData
          ? `${dashboardData.average_waiting_time} min`
          : "..."}
      </strong>
      <p>Based on current queue</p>
    </div>

    <div className="report-card">
      <span>Queue Efficiency</span>
      <strong>86%</strong>
      <p>Good performance</p>
    </div>

  </div>

  {/* Procurement Summary */}
  <div className="report-table">

    <h3>🌾 Procurement Summary</h3>

    <table>

      <thead>
        <tr>
          <th>Centre</th>
          <th>Procurement</th>
          <th>Target</th>
          <th>Achievement</th>
        </tr>
      </thead>

      <tbody>

        <tr>
          <td>Bhimavaram Centre</td>
          <td>720 Q</td>
          <td>1000 Q</td>
          <td>72%</td>
        </tr>

        <tr>
          <td>Tanuku Centre</td>
          <td>650 Q</td>
          <td>900 Q</td>
          <td>72%</td>
        </tr>

        <tr>
          <td>Palakollu Centre</td>
          <td>810 Q</td>
          <td>1000 Q</td>
          <td>81%</td>
        </tr>

        <tr>
          <td>Narasapur Centre</td>
          <td>590 Q</td>
          <td>850 Q</td>
          <td>69%</td>
        </tr>

      </tbody>

    </table>

  </div>

  {/* Performance Indicators */}
  <div className="performance-indicators">

    <h3>📈 Performance Indicators</h3>

    <div className="indicator-item">
      <span>Procurement Target Achievement</span>

      <strong>
        {dashboardData
          ? `${Math.round(
              (dashboardData.procured / dashboardData.daily_target) * 100
            )}%`
          : "..."}
      </strong>
    </div>

    <div className="indicator-item">
      <span>Queue Efficiency</span>
      <strong>86%</strong>
    </div>

    <div className="indicator-item">
      <span>Centre Utilization</span>
      <strong>78%</strong>
    </div>

  </div>

</div>
      </main>

    </div>
    
  );
}

export default App;