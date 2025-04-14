<template>
  <div class="dashboard">
    <div class="info-cards">
      <!-- Card 1: Jumlah Perbaikan -->
      <div class="card">
        <div class="card-icon">
          <i class="bi bi-luggage-fill"></i>
        </div>
        <div class="card-content">
          <h3>{{ jumlahPerbaikan }}</h3>
          <p>Jumlah Perbaikan</p>
        </div>
      </div>

      <!-- Card 2: Jumlah Pelanggan -->
      <div class="card">
        <div class="card-icon">
          <i class="bi bi-people-fill"></i>
        </div>
        <div class="card-content">
          <h3>{{ jumlahPelanggan }}</h3>
          <p>Jumlah Pelanggan</p>
        </div>
      </div>

      <!-- Card 3: Jenis Material -->
      <div class="card">
        <div class="card-icon">
          <i class="bi bi-stack"></i>
        </div>
        <div class="card-content">
          <h3>{{ jenisBahan }}</h3>
          <p>Jenis Material</p>
        </div>
      </div>

      <!-- Card 4: Jumlah Layanan -->
      <div class="card">
        <div class="card-icon">
          <i class="bi bi-wrench-adjustable-circle"></i>
        </div>
        <div class="card-content">
          <h3>{{ jumlahLayanan }}</h3>
          <p>Jumlah Layanan</p>
        </div>
      </div>
    </div>

    <!-- Chart Section -->
    <div class="chart-container">
      <canvas id="repairChart" width="600" height="150"></canvas>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import Chart from 'chart.js/auto';

export default {
  setup() {
    const jumlahPerbaikan = ref(0);
    const jumlahPelanggan = ref(0);
    const jenisBahan = ref(0);
    const jumlahLayanan = ref(0);
    const chart = ref({ labels: [], data: [] });

    const convertToMonthName = (labels) => {
      return labels.map((label) => {
        const [year, month] = label.split('-');
        const date = new Date(year, month - 1);
        return `${date.toLocaleString('id-ID', { month: 'long', year: 'numeric' })}`;
      });
    };

    const fetchDashboardData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:50/dashboard');
        if (!response.ok) {
          throw new Error(`HTTP Error: ${response.status}`);
        }
        const data = await response.json();
        jumlahPerbaikan.value = data['jumlah Perbaikan'];
        jumlahPelanggan.value = data['jumlah Pelanggan'];
        jenisBahan.value = data['jenis Bahan'];
        jumlahLayanan.value = data['jumlah Pemasok'];
        chart.value.labels = convertToMonthName(data.chartData.labels);
        chart.value.data = data.chartData.data;
        createChart();
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      }
    };

    const createChart = () => {
      const ctx = document.getElementById('repairChart').getContext('2d');
      if (!chart.value.labels.length || !chart.value.data.length) {
        console.warn('Chart data or labels are empty.');
        return;
      }

      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: chart.value.labels,
          datasets: [
            {
              label: 'Perbaikan Tahun 2024',
              data: chart.value.data,
              backgroundColor: 'rgba(38, 185, 154, 0.7)',
              borderColor: 'rgba(38, 185, 154, 0.7)',
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
            },
          },
          scales: {
            x: { beginAtZero: true },
            y: { beginAtZero: true },
          },
          barThickness: 30,
          barPercentage: 0.8,
        },
      });
    };

    onMounted(fetchDashboardData);

    return { jumlahPerbaikan, jumlahPelanggan, jenisBahan, jumlahLayanan, chart };
  },
};
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.info-cards {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 30px;
}

.card {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  text-align: center;
  flex: 1;
  max-width: 300px;
}

.card-icon {
  font-size: 30px;
  color: #4CAF50;
  margin-bottom: 10px;
}

.card-content h3 {
  font-size: 24px;
  margin: 0;
  color: #333333;
}

.card-content p {
  font-size: 16px;
  margin: 5px 0 0;
  color: #777777;
}

.chart-container {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}
</style>
