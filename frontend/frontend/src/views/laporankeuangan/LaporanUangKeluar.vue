<template>
  <div class="content">
    <div class="container-fluid">
      <div style="margin-bottom: 20px;">
        <button class="btn btn-link" style="color: black;" @click="showUangMasuk">Uang Masuk</button>
        <button class="btn btn-link" style="color: black;" @click="showUangKeluar">Uang Keluar</button>
      </div>
      <!-- Filter and Search -->
      <div class="d-flex justify-content-between mt-3">
        <div class="d-flex">
          <input type="date" v-model="startDate" class="form-control" @change="filterByDate" />
          <input type="date" v-model="endDate" class="form-control ml-2" @change="filterByDate" />
        </div>
      </div>
      <div class="row">
        <div class="col-md-12">
          <div class="card strpied-tabled-with-hover shadow">
            <div class="card-header">
              <div class="d-flex justify-content-between align-items-center">
                <h4 class="card-title">Laporan Uang Keluar</h4>
              </div>
            </div>
            <div class="card-body table-full-width table-responsive">
              <table class="table table-hover" ref="tableToPrint">
                <thead>
                  <tr>
                    <th>No</th>
                    <th>Tanggal</th>
                    <th>Jenis Pengeluaran</th>
                    <th>Total Pengeluaran</th>
                    <th>Deskripsi</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(laporan_keuangan, index) in paginatedLayanan" :key="laporan_keuangan.pengeluaran_id">
                    <td>{{ index + 1 }}</td>
                    <td>{{ laporan_keuangan.tanggal ? new Date(laporan_keuangan.tanggal).toLocaleDateString('id-ID') :
                      '' }}</td>
                    <td>{{ laporan_keuangan.jenis_pengeluaran }}</td>
                    <td>{{ formatRupiah(laporan_keuangan.total_pengeluaran) }}</td>
                    <td>{{laporan_keuangan.keterangan}}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <!-- Pagination -->
            <nav aria-label="Table Pagination">
              <ul class="pagination">
                <li class="page-item" :class="{ disabled: currentPage === 1 }">
                  <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">Previous</a>
                </li>
                <li class="page-item" :class="{ active: page === currentPage }" v-for="page in totalPages" :key="page">
                  <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
                </li>
                <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                  <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">Next</a>
                </li>
              </ul>
            </nav>
            <!-- Print Button -->
            <div class="d-flex justify-content-start mt-3 mb-3 ml-3">
              <button class="btn btn-success btn-fill" @click="printTable">Cetak</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  border: 1px solid #e3e3e3;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-header {
  background-color: #f8f9fa;
  font-weight: bold;
}

.table-hover tbody tr:hover {
  background-color: #f1f1f1;
}

.pagination {
  justify-content: right;
  margin-top: 15px;
  margin-right: 15px;
}

.page-link {
  color: #007bff;
}

.page-item.active .page-link {
  background-color: #007bff;
  border-color: #007bff;
}

.page-item.disabled .page-link {
  color: #6c757d;
  pointer-events: none;
}

.action-button {
  margin-right: 10px;
}

input[type="date"] {
  width: 180px;
}

input[type="text"] {
  width: 200px;
}
</style>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      api: 'http://localhost:50/pengeluaran', // Endpoint API untuk laporan uang keluar
      laporan_keuangan: [],
      currentPage: 1,
      itemsPerPage: 10,
      startDate: '',
      endDate: '',
      filteredLaporanKeuangan: [],
    };
  },

  computed: {
    totalPages() {
      return Math.ceil(this.filteredLaporanKeuangan.length / this.itemsPerPage);
    },
    paginatedLayanan() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredLaporanKeuangan.slice(start, end);
    },
  },

  mounted() {
    this.getLaporanKeuangan();
  },

  methods: {
    getLaporanKeuangan() {
      axios.get(this.api)
        .then(response => {
          console.log('Data response:', response.data);  // Periksa struktur respons
          const laporanKeuangan = response.data.message; // Jika data berada di dalam 'message'
          if (Array.isArray(laporanKeuangan)) {
            this.laporan_keuangan = laporanKeuangan;
            this.filteredLaporanKeuangan = laporanKeuangan; // Inisialisasi data yang sudah difilter
          } else {
            console.log('Data tidak berupa array:', laporanKeuangan);
          }
        })
        .catch(error => {
          console.log('Error fetching data:', error);
        });
    },
    formatRupiah(value) {
      const number = Number(value);
      if (isNaN(number)) return "-";
      return new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR" }).format(number);
    },
    changePage(page) {
      this.currentPage = page;
    },
    filterByDate() {
      const start = this.startDate ? new Date(this.startDate).getTime() : 0;
      const end = this.endDate ? new Date(this.endDate).getTime() : Date.now();

      this.filteredLaporanKeuangan = this.laporan_keuangan.filter(item => {
        const itemDate = new Date(item.tanggal).getTime();
        return itemDate >= start && itemDate <= end;
      });

      this.currentPage = 1; // Reset to the first page
    },
    showUangMasuk() {
      // Logic for showing "Uang Keluar" data
      this.$router.push('/laporankeuangan');
    },
    printTable() {
      const printWindow = window.open('', '', 'width=800,height=600');
      printWindow.document.write('<html><head><title>Print Laporan</title></head><body>');
      printWindow.document.write(this.$refs.tableToPrint.innerHTML); // Target the table content
      printWindow.document.write('</body></html>');
      printWindow.document.close();
      printWindow.print();
    }
  }
};
</script>
