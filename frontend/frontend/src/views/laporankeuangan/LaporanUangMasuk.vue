<template>
  <div class="content">
    <div class="container-fluid">
      <div style="margin-bottom: 20px;">
        <button class="btn btn-link" :class="{ active: activeTab === 'uangMasuk' }" style="color: black;"
          @click="setActiveTab('uangMasuk')">
          Uang Masuk
        </button>
        <button class="btn btn-link" :class="{ active: activeTab === 'uangKeluar' }" style="color: black;"
          @click="setActiveTab('uangKeluar')">
          Uang Keluar
        </button>
      </div>
      <!-- Filter and Search -->
      <div class="d-flex justify-content-between mt-3">
        <div class="d-flex">
          <input type="date" v-model="startDate" class="form-control" @change="filterByDate" />
          <input type="date" v-model="endDate" class="form-control ml-2" @change="filterByDate" />
        </div>
        <div>
          <input type="text" v-model="searchQuery" class="form-control ml-2" placeholder="Search..."
            @input="filterSearch" />
        </div>
      </div>
      <div class="row">
        <div class="col-md-12">
          <div class="card strpied-tabled-with-hover shadow">
            <div class="card-header">
              <div class="d-flex justify-content-between align-items-center">
                <h4 class="card-title">Laporan Uang Masuk</h4>
              </div>
            </div>
            <div class="card-body table-full-width table-responsive">
              <table class="table table-hover" ref="tableToPrint">
                <thead>
                  <tr>
                    <th>No</th>
                    <th>Kode Perbaikan</th>
                    <th>Tanggal</th>
                    <th>Total Uang Masuk</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(laporan_keuangan, index) in paginatedLayanan" :key="laporan_keuangan.laporan_id">
                    <td>{{ index + 1 }}</td>
                    <td>{{ laporan_keuangan.kode_perbaikan }}</td>
                    <td>{{ laporan_keuangan.tanggal_laporan ? new
                      Date(laporan_keuangan.tanggal_laporan).toLocaleDateString('id-ID', {
                        year: 'numeric', month: 'numeric', day: 'numeric'
                      }) : '' }}</td>
                    <td>{{ formatRupiah(laporan_keuangan.pendapatan) }}</td>
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
              <button class="btn btn-success btn-fill" @click="printTable">Cetak PDF</button>
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

.btn-link.active {
  font-weight: bold;
  text-decoration: underline;
  color: blue;
  /* Warna teks saat aktif */
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
import html2pdf from 'html2pdf.js';

export default {
  data() {
    return {
      api: 'http://localhost:50/laporanKeuangan', // Endpoint API
      laporan_keuangan: [],
      currentPage: 1,
      itemsPerPage: 20,
      startDate: '',
      endDate: '',
      searchQuery: '',
      activeTab: 'uangMasuk',
      filteredLaporanKeuangan: [],
      searchQuery: '',
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
    filterSearch() {
      this.filteredLaporanKeuangan = this.laporan_keuangan.filter(item => {
        return item.kode_perbaikan.toLowerCase().includes(this.searchQuery.toLowerCase());
      });
      this.currentPage = 1; // Reset to the first page
    },
    getLaporanKeuangan() {
      axios.get(this.api)
        .then(response => {
          const laporanKeuangan = response.data["Laporan Keuangan"];
          if (Array.isArray(laporanKeuangan)) {
            this.laporan_keuangan = laporanKeuangan.sort((a, b) => {
              return new Date(b.tanggal_laporan) - new Date(a.tanggal_laporan); // Descending
            });
            this.filteredLaporanKeuangan = [...this.laporan_keuangan]; // Initialize filtered data
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
      const start = this.startDate ? new Date(this.startDate).setHours(0, 0, 0, 0) : null;
      const end = this.endDate ? new Date(this.endDate).setHours(23, 59, 59, 999) : null;

      this.filteredLaporanKeuangan = this.laporan_keuangan.filter(item => {
        const itemDate = new Date(item.tanggal_laporan).getTime();

        if (start && end) {
          // Jika rentang waktu dipilih
          return itemDate >= start && itemDate <= end;
        } else if (start) {
          // Jika hanya startDate yang dipilih, filter untuk satu hari tersebut
          const endOfDay = new Date(this.startDate).setHours(23, 59, 59, 999);
          return itemDate >= start && itemDate <= endOfDay;
        } else {
          // Jika tidak ada filter
          return true;
        }
      });

      this.currentPage = 1; // Reset ke halaman pertama
    },
    filterSearch() {
      this.filteredLaporanKeuangan = this.laporan_keuangan.filter(item => {
        return item.kode_perbaikan.toLowerCase().includes(this.searchQuery.toLowerCase());
      });
      this.currentPage = 1; // Reset to the first page
    },
    setActiveTab(tab) {
      this.activeTab = tab;
      if (tab === 'uangMasuk') {
        this.showUangMasuk();
      } else if (tab === 'uangKeluar') {
        this.showUangKeluar();
      }
    },
    showUangMasuk() {
      // Logic for showing "Uang Masuk" data
      this.$router.push({ path: '/laporankeuangan', replace: true });// Re-fetch data for "Uang Masuk"
    },
    showUangKeluar() {
      // Logic for showing "Uang Keluar" data
      this.$router.push({ path: '/pengeluaran', replace: true });
    },
    calculateTotalUangMasuk() {
      // Hitung total pendapatan dari data yang sudah difilter
      return this.filteredLaporanKeuangan.reduce((total, item) => {
        return total + (Number(item.pendapatan) || 0);
      }, 0);
    },
    printTable() {
      // Buat elemen baru untuk menyertakan total uang masuk
      const tableElement = this.$refs.tableToPrint.cloneNode(true); // Salin tabel untuk modifikasi
      const totalRow = document.createElement('tr');
      totalRow.innerHTML = `
      <td colspan="3" style="font-weight: bold; text-align: right;">Total Uang Masuk:</td>
      <td style="font-weight: bold;">${this.formatRupiah(this.calculateTotalUangMasuk())}</td>
    `;
      tableElement.querySelector('tbody').appendChild(totalRow); // Tambahkan total ke tabel

      // Opsi untuk PDF
      const options = {
        margin: 10,
        filename: 'Laporan_Uang_Masuk.pdf',
        html2canvas: { scale: 2 },
        jsPDF: { orientation: 'portrait' },
      };

      // Cetak ke PDF
      html2pdf().set(options).from(tableElement).save();
    }
  }
};
</script>
