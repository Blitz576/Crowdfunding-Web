<template>
  <section class="row justify-content-center">
    <form
      class="container row align-items-center flex-column needs-validation"
      novalidate
      @submit.prevent="addProject"
    >
      <div
        class="container p-5 row align-items-center flex-column gap-2 w-50 m-1 rounded"
        style="background-color: rgb(91 91 91 / 50%) !important"
      >
        <div class="form-floating">
          <input
            type="text"
            class="form-control"
            name="title"
            id="title"
            placeholder="title"
            v-model="title"
            required
            pattern="[A-Za-z0-9\s]{1,50}"
          />
          <label for="title" class="text-dark ms-2">Project Title</label>
          <div class="invalid-feedback">
            Please provide a valid title ( less than 50 letters ) .
          </div>
        </div>

        <div class="form-floating">
          <input
            type="number"
            class="form-control"
            id="target"
            name="target"
            placeholder="target"
            v-model="targetMoney"
            required
            min="1"
           
          />
          <label for="target" class="text-dark ms-2">Target Money</label>
          <div class="invalid-feedback">
            Please provide a target amount ( Number ) .
          </div>
        </div>

        <div class="form-floating">
          <textarea
            class="form-control"
            name="description"
            id="description"
            placeholder="description"
            v-model="description"
            style="height: 100px"
            required
          ></textarea>
          <label for="description" class="text-dark ms-2"
            >Project Description</label
          >
          <div class="invalid-feedback">
            Please provide a valid description ( less than 400 letters).
          </div>
        </div>

        <div class="form-floating">
          <select
            class="form-select"
            name="category"
            id="category"
            v-model="categoryResult"
            required
          >
            <option selected disabled hidden value="">
              Please select a category
            </option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </option>
          </select>
          <label for="category" class="text-dark ms-2">Category</label>
          <div class="invalid-feedback">Please select a category.</div>
        </div>
        <div class="form-floating">
         
          <select @change="addSelection" style="width: 100%; z-index: 100;" ref="select" class=" form-control select2" multiple id="validationCustom05" 
                    pattern="^[a-zA-Z ,.'\-]+$" v-model="projectTags">
                  </select>
          <div class="invalid-feedback">Please select tags .</div>
        </div>

        <div class="form-floating">
          <input
            type="date"
            class="form-control "
            name="endDate"
            id="endDate"
            placeholder="endDate"
            v-model="endDate"
            required
          />
          <label for="endDate" class="text-dark ms-2">Project End Date</label>
          <div v-if="invalidEndDate" class="invalid-feedback">please choose End date (must be later.)</div>
        </div>
        <div class="input-style">
          <label class="input-group-text" for="photo"
            >Upload multiple photo</label
          >
          <input
            type="file"
            class="form-control"
            id="photo"
            multiple
            @change="takePhotos($event)"
          />
        </div>

        <input type="submit" value="Add" class="btn col-3" />
      </div>
    </form>
  </section>
</template>
<script>
import { datastore } from '@/stors/crowdfundingStore';
import FunctionsClass from "../assets/js/registerAndUpdate";
const functionsObject = new FunctionsClass();

export default {
  data: () => ({
    storData: datastore(),
    title: "",
    description: "",
    targetMoney: "",
    categoryResult: "",
    endDate:"",
    invalidEndDate: false,
    categories: [],
    tags: [],
    selectedTags: [],
    userInfo:
      JSON.parse(localStorage.getItem("userInfo")) ||
      JSON.parse(sessionStorage.getItem("userInfo")),
    images: [],
  }),
  methods: {
    async addProject($event) {
      const formData = {
        title: this.title,
        description: this.description,
        endDate: this.endDate,
      };
      const projectValidationResult =
      functionsObject.projectValidations(formData);
      const HTMLValidationResult = functionsObject.HTMLValidations($event);
      this.invalidEndDate = !this.isValidEndDate(this.endDate);

      if (projectValidationResult && HTMLValidationResult) {
        const formData = this.prepareFormData();
        try {
          const responseData = await this.sendProjectRequest(formData);
          console.log("Project added successfully!");
          this.$router.push(`/projects/${responseData.id}`);
        } catch (error) {
          console.error("Error adding project:", error);
        }
      }
    },
    isValidEndDate(endDate) {
      if( new Date(endDate) > new Date()){
        return true;
      }else{
        this.endDate="";
      }
    },

    prepareFormData() {
      const currentDate = new Date();
      const startDate = currentDate.toISOString().split("T")[0];
      const userInfo =
        JSON.parse(localStorage.getItem("userInfo")) ||
        JSON.parse(sessionStorage.getItem("userInfo"));
      const token = userInfo.token;

      const form = new FormData();
      form.append("owner_id", userInfo["user_id"]);
      form.append("category_id", this.categoryResult);
      form.append("title", this.title);
      form.append("description", this.description);
      form.append("end_date", this.endDate);
      form.append("target_money", this.targetMoney);
      for (let i = 0; i < this.images.length; i++) {
        form.append("photos", this.images[i]);
      }
      for (let i = 0; i < this.selectedTags.length; i++) {
        form.append("tages", this.selectedTags[i]);
      }
      return { form, token };
    },

    async sendProjectRequest(formData) {
      const response = await fetch("http://127.0.0.1:8000/api/projects/", {
        method: "POST",
        headers: {
          Authorization: `token ${formData.token}`,
        },
        body: formData.form,
      });

      return await response.json();
    },

    takePhotos(event) {
      const selectedImages = event.target.files;
      for (let i = 0; i < selectedImages.length; i++) {
        const file = selectedImages[i];
        this.images.push(file);
      }
    },
  },

async created() {
    await this.storData.getCategories();
    await this.storData.getTags();
    this.categories = this.storData.categories;
    this.tags = this.storData.tags;
    functionsObject.tagSelection(this);
  },
};
</script>
<style scoped>
.form-control:focus,
select:focus {
  border-color: #28a745 !important;
  box-shadow: 0 0 0 0.2rem rgba(40, 167, 69, 0.25) !important;
}
.btn,
.btn:hover,
.btn:active,
.btn:visited {
  color: #dadee2;
  background-color: #246137;
  border-color: #246137;
}
p {
  color: #dbdcdc;
  text-align: center;
}
.form-floating {
  opacity: 0.6;
}
.input-style,
.form-floating,
.photos {
  opacity: 0.8;
}
.container {
  padding: 2.5rem 3rem !important;
}

</style>
