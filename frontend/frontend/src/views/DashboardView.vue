<template>
  <div class="dashboard">
    <div class="chart-container" style="background-color: white;">
      <canvas id="repairChart" width="600" height="300"></canvas>
    </div>
    <div class="info-cards">
      <div class="card">Jumlah Perbaikan: {{ jumlahPerbaikan }}</div>
      <div class="card">Jumlah Pelanggan: {{ jumlahPelanggan }}</div>
      <div class="card">Jenis Material: {{ jenisBahan }}</div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import Chart from 'chart.js/auto';

export default {
  setup() {
    // Define reactive properties
    const jumlahPerbaikan = ref(0);
    const jumlahPelanggan = ref(0);
    const jenisBahan = ref(0);
    const chart = ref({ labels: [], data: [] });
    const convertToMonthName = (labels) => {
      return labels.map((label) => {
        const [year, month] = label.split('-'); // Pisahkan tahun dan bulan
        const date = new Date(year, month - 1); // Buat objek tanggal (bulan mulai dari 0)
        return `${date.toLocaleString('id-ID', { month: 'long' })}`; // Format menjadi "Nama Bulan Tahun"
      });
    };

    // Fetch data from the backend API
    const fetchDashboardData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:50/dashboard');
        if (!response.ok) {
          throw new Error(`HTTP Error: ${response.status}`);
        }
        const data = await response.json();

        // Update reactive properties with fetched data
        jumlahPerbaikan.value = data['jumlah Perbaikan'];
        jumlahPelanggan.value = data['jumlah Pelanggan'];
        jenisBahan.value = data['jenis Bahan'];

        // Update chart data with the correct structure
        chart.value.labels = convertToMonthName(data.chartData.labels); // Ambil labels dari chartData
        chart.value.data = data.chartData.data; // Ambil data dari chartData

        // Create chart with updated data
        createChart();
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      }
    };

    // Create a chart using Chart.js
    const createChart = () => {
      const ctx = document.getElementById('repairChart').getContext('2d');

      if (!chart.value.labels.length || !chart.value.data.length) {
        console.warn('Chart data or labels are empty.');
        return; // Jangan buat chart jika tidak ada data
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
            x: {
              ticks: {
                display: true,
              },
              beginAtZero: true,
            },
            y: {
              beginAtZero: true,
            },
          },
          barThickness: 30,
          barPercentage: 0.8,
        },
      });
    };

    // Lifecycle hook to fetch data when the component is mounted
    onMounted(() => {
      fetchDashboardData();
    });

    return { jumlahPerbaikan, jumlahPelanggan, jenisBahan, chart };
  },
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  max-width: 800px;
  margin: 20px auto;
}

.info-cards {
  display: flex;
  justify-content: space-around;
  margin-top: 30px;
}

.card {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  width: 200px;
}
</style>