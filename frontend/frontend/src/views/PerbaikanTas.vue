<template>
    <div class="content">
        <div class="container-fluid">
            <div class="row">
                <div class="card" style="width: 80%;">
                    <div class="card-header">
                        <h4 class="card-title">Perbaikan Baru</h4>
                    </div>
                    <div class="card-body">
                        <form @submit.prevent="handleSubmit">
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label>Nama Pelanggan</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <select class="form-control" v-model="customerName" required>
                                            <option selected>Choose...</option>
                                            <option>...</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-2 pr-1">
                                    <div class="form-group">
                                        <label>Jenis Perbaikan</label>
                                    </div>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <select class="form-control" v-model="jenisPerbaikan" required>
                                            <option selected>Choose...</option>
                                            <option>...</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                            <!-- <div class="row">
                                <div class="col-md-2">
                                    <label>About Me</label>
                                </div>
                                <div class="col-md-10">
                                    <div class="form-group">
                                        <textarea rows="4" cols="80" class="form-control"
                                            placeholder="Here can be your description"
                                            value="Mike">Lamborghini Mercy, Your chick she so thirsty, I'm in that two seat Lambo.</textarea>
                                    </div>
                                </div>
                            </div> -->
                            <button type="submit" class="btn btn-info btn-fill pull-right">Update Profile</button>
                            <div class="clearfix"></div>
                        </form>
                        <!-- <form>
                            <div class="form-group row">
                                <label for="company" class="col-sm-2 col-form-label">Company</label>
                                <div class="col-sm-10">
                                    <input type="text" class="form-control" id="company" placeholder="Company"
                                        value="Creative Code Inc." disabled>
                                </div>
                            </div>
                            <div class="form-group row">
                                <label for="username" class="col-sm-2 col-form-label">Username</label>
                                <div class="col-sm-10">
                                    <input type="text" class="form-control" id="username" placeholder="Username"
                                        value="michael23">
                                </div>
                            </div>
                            <div class="form-group row">
                                <label for="email" class="col-sm-2 col-form-label">Email address</label>
                                <div class="col-sm-10">
                                    <input type="email" class="form-control" id="email" placeholder="Email">
                                </div>
                            </div>
                            <div class="form-group row">
                                <label for="firstName" class="col-sm-2 col-form-label">First Name</label>
                                <div class="col-sm-10">
                                    <input type="text" class="form-control" id="firstName" placeholder="First Name"
                                        value="Mike">
                                </div>
                            </div>
                            <div class="form-group row">
                                <label for="lastName" class="col-sm-2 col-form-label">Last Name</label>
                                <div class="col-sm-10">
                                    <input type="text" class="form-control" id="lastName" placeholder="Last Name"
                                        value="Andrew">
                                </div>
                            </div>
                            <div class="form-group row">
                                <label for="address" class="col-sm-2 col-form-label">Address</label>
                                <div class="col-sm-10">
                                    <input type="text" class="form-control" id="address" placeholder="Home Address"
                                        value="Bld Mihail Kogalniceanu, nr. 8 Bl 1, Sc 1, Ap 09">
                                </div>
                            </div>
                            <div class="form-group row">
                                <label for="city" class="col-sm-2 col-form-label">City</label>
                                <div class="col-sm-10">
                                    <input type="text" class="form-control" id="city" placeholder="City" value="Mike">
                                </div>
                            </div>
                            <div class="form-group row">
                                <label for="country" class="col-sm-2 col-form-label">Country</label>
                                <div class="col-sm-10">
                                    <input type="text" class="form-control" id="country" placeholder="Country"
                                        value="Andrew">
                                </div>
                            </div>
                            <div class="form-group row">
                                <label for="postalCode" class="col-sm-2 col-form-label">Postal Code</label>
                                <div class="col-sm-10">
                                    <input type="number" class="form-control" id="postalCode" placeholder="ZIP Code">
                                </div>
                            </div>
                            <div class="form-group row">
                                <label for="aboutMe" class="col-sm-2 col-form-label">About Me</label>
                                <div class="col-sm-10">
                                    <textarea rows="4" class="form-control" id="aboutMe"
                                        placeholder="Here can be your description">Lamborghini Mercy, Your chick she so thirsty, I'm in that two seat Lambo.</textarea>
                                </div>
                            </div>
                            <button type="submit" class="btn btn-info btn-fill pull-right">Update Profile</button>
                            <div class="clearfix"></div>
                        </form> -->

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
            customerName: '',
            jenisPerbaikan: ''
        };
    },
    methods: {
        handleSubmit() {
            // Logika untuk menangani pengiriman form
            if (this.customerName && this.jenisPerbaikan) {
                console.log('Form dikirim:', {
                    customerName: this.customerName,
                    jenisPerbaikan: this.jenisPerbaikan
                });
                // Reset form atau melakukan tindakan lain
                this.customerName = '';
                this.jenisPerbaikan = '';
            } else {
                alert('Silakan isi semua kolom yang wajib.');
            }
        }
    }
}
</script>