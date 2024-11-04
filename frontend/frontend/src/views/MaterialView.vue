<template>
    <div class="content">
      <div class="container-fluid">
        <div class="row">
          <div class="col-md-12">
            <div class="card strpied-tabled-with-hover">
              <div class="card-header">
                <h4 class="card-title">Striped Table with Hover</h4>
                <p class="card-category">Here is a subtitle for this table</p>
              </div>
              <div class="card-body table-full-width table-responsive">
                <table class="table table-hover table-striped">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Name</th>
                      <th>Salary</th>
                      <th>Country</th>
                      <th>City</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(item, index) in tableData" :key="index">
                      <td>{{ item.id }}</td>
                      <td>{{ item.name }}</td>
                      <td>{{ item.salary }}</td>
                      <td>{{ item.country }}</td>
                      <td>{{ item.city }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        tableData: [
          { id: 1, name: "Dakota Rice", salary: "$36,738", country: "Niger", city: "Oud-Turnhout" },
          { id: 2, name: "Minerva Hooper", salary: "$23,789", country: "Curaçao", city: "Sinaai-Waas" },
          { id: 3, name: "Sage Rodriguez", salary: "$56,142", country: "Netherlands", city: "Baileux" },
          { id: 4, name: "Philip Chaney", salary: "$38,735", country: "Korea, South", city: "Overland Park" },
          { id: 5, name: "Doris Greene", salary: "$63,542", country: "Malawi", city: "Feldkirchen in Kärnten" },
          { id: 6, name: "Mason Porter", salary: "$78,615", country: "Chile", city: "Gloucester" }
        ]
      };
    }
  };
  </script>

  