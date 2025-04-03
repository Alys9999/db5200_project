const BASE_URL = "https://db-group5-452710.wl.r.appspot.com";

console.log("Frontend loaded!");

function fetchLowStock() {
  const threshold = document.getElementById("stockThreshold").value || 10;

  fetch(`/products/low-stock/${threshold}`)
    .then(res => res.json())
    .then(data => {
      const list = document.getElementById("lowStockList");
      list.innerHTML = '';
      data.forEach(p => {
        list.innerHTML += `<li><strong>${p.name}</strong> (Stock: ${p.stock_quantity})</li>`;
      });
    })
    .catch(err => {
      console.error("Error fetching low stock:", err);
      alert("Failed to fetch low stock products.");
    });
}

function fetchBestSellers() {
  const days = document.getElementById("days").value || 30;
  const limit = document.getElementById("limit").value || 5;

  fetch(`/products/best-selling/${days}/${limit}`)

    .then(res => res.json())
    .then(data => {
      const list = document.getElementById("bestSellersList");
      list.innerHTML = '';
      data.forEach(p => {
        list.innerHTML += `<li><strong>${p.name}</strong> - ${p.total_sold} sold</li>`;
      });
    })
    .catch(err => {
      console.error("Error fetching best sellers:", err);
      alert("Failed to fetch best selling products.");
    });
}

function fetchRevenue() {
  const days = document.getElementById("revenueDays").value || 30;

  fetch(`/revenue/${days}`)

    .then(res => res.json())
    .then(data => {
      const total = data.total_revenue ?? 0;
      document.getElementById("revenueDisplay").innerText =
        `Total Revenue (last ${days} days): $${parseFloat(total).toFixed(2)}`;
    })
    .catch(err => {
      console.error("Error fetching revenue:", err);
      alert("Failed to fetch revenue.");
    });
}

function login() {
    const username = document.getElementById("loginUsername").value;
    const password = document.getElementById("loginPassword").value;
  
    fetch(`/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
      credentials: "include"
    })
      .then(res => {
        if (!res.ok) throw new Error("Login failed");
        return res.json();
      })
      .then(data => {
        document.getElementById("loginStatus").innerText = `Logged in as ${data.user}`;
      })
      .catch(err => {
        console.error(err);
        document.getElementById("loginStatus").innerText = "Login failed";
      });
  }
  
  function logout() {
    fetch(`/logout`, { method: "POST" })

      .then(() => {
        // Go back to login page
        window.location.href = "/";
      });
  }

// Fetch Orders by Status
function fetchOrdersByStatus() {
    const status = document.getElementById("orderStatus").value;
   
    fetch(`/orders/status/${status}`)
        .then(res => {
            if (!res.ok) throw new Error("Failed to fetch orders");
            return res.json();
        })
        .then(data => {
            const list = document.getElementById("ordersStatusList");
            list.innerHTML = "";
   
            if (data.length === 0) {
                list.innerHTML = "<li>No orders found for this status</li>";
                return;
            }
   
            data.forEach(order => {
                const orderDate = new Date(order.order_date).toLocaleDateString();
                list.innerHTML += `
                    <li class="order-item">
                        <div class="order-header">
                            <span>Order #${order.order_id}</span>
                            <span class="status-badge ${order.status.toLowerCase()}">
                                ${order.status}
                            </span>
                        </div>
                        <div class="order-details">
                            <span>Date: ${orderDate}</span>
                            <span>Total: $${order.total_amount.toFixed(2)}</span>
                        </div>
                    </li>
                `;
            });
        })
        .catch(err => {
            console.error("Error fetching orders by status:", err);
            alert("Failed to fetch orders.");
        });
  }
   
  
   