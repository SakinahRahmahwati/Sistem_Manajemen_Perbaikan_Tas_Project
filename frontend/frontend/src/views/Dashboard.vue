<template>
  <div class="DashboardPage">
    <header
      class="navbar sticky-top bg-dark flex-md-nowrap p-0 shadow"
      data-bs-theme="dark"
    >
      <a
        class="navbar-brand col-md-3 col-lg-2 me-0 px-3 fs-6 text-white"
        href="#"
        >Company name</a
      >

      <ul class="navbar-nav flex-row d-md-none">
        <li class="nav-item text-nowrap">
          <button
            class="nav-link px-3 text-white"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSearch"
            aria-controls="navbarSearch"
            aria-expanded="false"
            aria-label="Toggle search"
          >
            <svg class="bi"><use xlink:href="#search" /></svg>
          </button>
        </li>
        <li class="nav-item text-nowrap">
          <button
            class="nav-link px-3 text-white"
            type="button"
            data-bs-toggle="offcanvas"
            data-bs-target="#sidebarMenu"
            aria-controls="sidebarMenu"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <svg class="bi"><use xlink:href="#list" /></svg>
          </button>
        </li>
      </ul>

      <div id="navbarSearch" class="navbar-search w-100 collapse">
        <input
          class="form-control w-100 rounded-0 border-0"
          type="text"
          placeholder="Search"
          aria-label="Search"
        />
      </div>
    </header>
    <div class="container-fluid">
      <div class="row">
        <div
          class="sidebar border border-right col-md-3 col-lg-2 p-0 bg-body-tertiary"
        >
          <div
            class="offcanvas-md offcanvas-end bg-body-tertiary"
            tabindex="-1"
            id="sidebarMenu"
            aria-labelledby="sidebarMenuLabel"
          >
            <div class="offcanvas-header">
              <h5 class="offcanvas-title" id="sidebarMenuLabel">
                Company name
              </h5>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="offcanvas"
                data-bs-target="#sidebarMenu"
                aria-label="Close"
              ></button>
            </div>
            <div
              class="offcanvas-body d-md-flex flex-column p-0 pt-lg-3 overflow-y-auto"
            >
              <ul class="nav flex-column">
                <li class="nav-item">
                  <a
                    class="nav-link d-flex align-items-center gap-2 active"
                    aria-current="page"
                    href="#"
                  >
                    <i class="bi bi-house-fill"></i>
                    Dashboard
                  </a>
                </li>
                <li class="nav-item">
                  <a class="nav-link d-flex align-items-center gap-2" href="#">
                    <i class="bi bi-file-earmark"></i>
                    Orders
                  </a>
                </li>
                <li class="nav-item">
                  <a class="nav-link d-flex align-items-center gap-2" href="#">
                    <svg class="bi"><use xlink:href="#cart"></use></svg>
                    Products
                  </a>
                </li>
                <li class="nav-item">
                  <a class="nav-link d-flex align-items-center gap-2" href="#">
                    <svg class="bi"><use xlink:href="#people"></use></svg>
                    Customers
                  </a>
                </li>
                <li class="nav-item">
                  <a class="nav-link d-flex align-items-center gap-2" href="#">
                    <svg class="bi"><use xlink:href="#graph-up"></use></svg>
                    Reports
                  </a>
                </li>
                <li class="nav-item">
                  <a class="nav-link d-flex align-items-center gap-2" href="#">
                    <svg class="bi"><use xlink:href="#puzzle"></use></svg>
                    Integrations
                  </a>
                </li>
              </ul>

              <h6
                class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-body-secondary text-uppercase"
              >
                <span>Saved reports</span>
                <a
                  class="link-secondary"
                  href="#"
                  aria-label="Add a new report"
                >
                  <svg class="bi"><use xlink:href="#plus-circle"></use></svg>
                </a>
              </h6>
              <ul class="nav flex-column mb-auto">
                <li class="nav-item">
                  <a class="nav-link d-flex align-items-center gap-2" href="#">
                    <svg class="bi">
                      <use xlink:href="#file-earmark-text"></use>
                    </svg>
                    Current month
                  </a>
                </li>
                <li class="nav-item">
                  <a class="nav-link d-flex align-items-center gap-2" href="#">
                    <svg class="bi">
                      <use xlink:href="#file-earmark-text"></use>
                    </svg>
                    Last quarter
                  </a>
                </li>
                <li class="nav-item">
                  <a class="nav-link d-flex align-items-center gap-2" href="#">
                    <svg class="bi">
                      <use xlink:href="#file-earmark-text"></use>
                    </svg>
                    Social engagement
                  </a>
                </li>
                <li class="nav-item">
                  <a class="nav-link d-flex align-items-center gap-2" href="#">
                    <svg class="bi">
                      <use xlink:href="#file-earmark-text"></use>
                    </svg>
                    Year-end sale
                  </a>
                </li>
              </ul>

              <hr class="my-3" />

              <ul class="nav flex-column mb-auto">
                <li class="nav-item">
                  <a class="nav-link d-flex align-items-center gap-2" href="#">
                    <svg class="bi">
                      <use xlink:href="#gear-wide-connected"></use>
                    </svg>
                    Settings
                  </a>
                </li>
                <li class="nav-item">
                  <a class="nav-link d-flex align-items-center gap-2" href="#">
                    <svg class="bi"><use xlink:href="#door-closed"></use></svg>
                    Sign out
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
          <div
            class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom"
          >
            <h1 class="h2">Dashboard</h1>
          </div>
          <canvas
            class="my-4 w-100"
            id="myChart"
            width="844"
            height="356"
            style="
              display: block;
              box-sizing: border-box;
              height: 285px;
              width: 675px;
            "
          ></canvas>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "DashboardPage",
  // ...
};
</script>
