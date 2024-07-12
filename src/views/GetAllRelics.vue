<template>
  <div>
    <el-form :inline="true" :model="formInline" class="demo-form-inline">
      <el-button type="info" @click="showInsertDialog" plain>添加信息</el-button>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      <el-form-item label="文物名称">
        <el-input v-model="formInline.name" placeholder="文物名称"></el-input>
      </el-form-item>
      <el-form-item label="年代">
        <el-select v-model="formInline.date" placeholder="请选择年代">
          <el-option
              v-for="date in dates"
              :key="date"
              :label="date"
              :value="date"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="博物馆">
        <el-select v-model="formInline.museum" placeholder="请选择博物馆">
          <el-option
              v-for="museum in museums"
              :key="museum.id"
              :label="museum.name"
              :value="museum.id"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">查询</el-button>
      </el-form-item>
    </el-form>

    <div>  <!--class="east-museum-container"-->
      <el-table :data="tableData" style="width: 100%">
        <el-table-column prop="name" label="文物名称" width="150"></el-table-column>
        <el-table-column prop="category" label="分类" width="140"></el-table-column>
        <el-table-column prop="image" label="图片" width="180">
          <template slot-scope="scope">
            <el-image
                style="width: 100px; height: 100px"
                :src="scope.row.image"
            ></el-image>
          </template>
        </el-table-column>
        <el-table-column prop="date" label="年代" width="140"></el-table-column>
        <el-table-column prop="museum" label="博物馆" width="150"></el-table-column>
        <el-table-column prop="location" label="位置" width="150"></el-table-column>
        <el-table-column prop="status" label="状态" width="140">
          <template slot-scope="scope">
            <span>{{ scope.row.status === 1 ? '展出' : '未展出' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template slot-scope="scope">
            <el-button @click="handleEdit(scope.row)" type="primary" size="small">修改</el-button>
            <el-popconfirm
                title="这是一段内容确定删除吗？"
                @confirm="deleteRelics(scope.row)"
            >
              <el-button slot="reference" type="danger" size="small">删除</el-button>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div class="block">
      <el-pagination
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-size="pageSize"
          :total="total">
      </el-pagination>
    </div>

    <el-dialog :visible.sync="dialogVisible" title="文物信息" width="500px">
      <el-form :model="form" label-width="100px" class="dialog-form">
        <el-form-item label="文物名称">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="form.category" placeholder="请选择博物馆">
            <el-option
                v-for="category in categories"
                :key="category.id"
                :label="category.name"
                :value="category.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="博物馆">
          <el-select v-model="form.museum" placeholder="请选择博物馆">
            <el-option
                v-for="museum in museums"
                :key="museum.id"
                :label="museum.name"
                :value="museum.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="年代">
          <el-input v-model="form.date"></el-input>
        </el-form-item>
        <el-form-item label="位置">
          <el-input v-model="form.location"></el-input>
        </el-form-item>
        <el-form-item label="图片">
          <el-upload
              ref="upload"
              action="/api/uploadFile"
              list-type="picture-card"
              :on-preview="handlePictureCardPreview"
              :on-remove="handleRemove"
              :on-change="UploadImage"
              :limit="1"
              :file-list="fileList"
              :auto-upload="false"
          >
            <i class="el-icon-plus"></i>
            <template #tip>
              <div style="font-size: 12px;color: #919191;">
                单次限制上传一张图片
              </div>
            </template>
          </el-upload>
          <el-dialog v-model="dialogVisible" style="line-height: 0;">
            <img style="width: 100%;height: 100%" :src="dialogImageUrl" alt=""/>
          </el-dialog>
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="form.status" :active-value="1" :inactive-value="0"></el-switch>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="isInsertMode ? insertRelics() : submitForm()">提交</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";

/* eslint-disable */  // 禁用整个脚本块的 ESLint 检查

export default {
  data() {
    return {
      dialogVisible: false,
      tableData: [],
      currentPage: 1,
      pageSize: 4,
      total: 0,
      formInline: {
        name: '',
        date: '',
        museum: '',
      },
      form: {
        name: '',
        category: '',
        image: '',
        date: '',
        location: '',
        status: '',
        museum: '',
      },
      form2: {
        name: '',
        category: '',
        image: '',
        date: '',
        location: '',
        status: '',
        museum: '',
      },
      dates: [],
      museums: [],
      categories: [],
      fileList: [], // 用于存储上传的文件
      editingIndex: -1,
      isInsertMode: false // 新增属性，用于区分插入和更新操作
    };
  },
  methods: {
    showInsertDialog() {
      this.dialogVisible = true;
      this.isInsertMode = true; // 设置为插入模式
      this.form = {
        name: '',
        category: '',
        image: '',
        date: '',
        location: '',
        status: '',
        museum: '',
      };
      this.fileList = [];
    },
    handleEdit(row) {
      this.dialogVisible = true;
      this.isInsertMode = false; // 设置为更新模式
      this.form = {...row};
      this.fileList = row.image ? [{name: 'image', url: row.image}] : [];
      this.editingIndex = this.tableData.indexOf(row);
    },
    onSubmit() {
      const {name, date, museum} = this.formInline;
      const params = {};

      if (name) params.name = name;
      if (date) params.date = date;
      if (museum) params.museum_id = museum;

      axios.get("/api/getRelics/", {params})
          .then(response => {
            this.tableData = response.data.data;
            this.pageSize = 4;
            this.total = response.data.total;
          })
          .catch(error => {
            console.error("Error fetching filtered relics data:", error);
          });
    },
    insertRelics() {
      axios.post("/api/insertRelics/", this.form)
          .then(() => {
            this.dialogVisible = false;
            alert("添加成功");
            this.fetchData();  // 重新获取数据，刷新列表
          })
          .catch(error => {
            console.error('Error inserting data:', error);
          });
    },
    deleteRelics(row) {
      axios.delete(`/api/deleteRelics/?name=${encodeURIComponent(row.name)}`)
          .then(() => {
            this.fetchData();
          })
          .catch(error => {
            console.error("Error deleting relics:", error);
          });
    },
    submitForm() {
      axios.post("/api/updateRelics/", this.form)
          .then(() => {
            this.$set(this.tableData, this.editingIndex, {...this.form});
            this.dialogVisible = false;
            alert("修改成功")
          })
          .catch(error => {
            console.error('Error updating data:', error);
          });
    },
    fetchData() {
      axios.get('/api/getRelics/', {
        params: {
          page: this.currentPage,
          page_size: this.pageSize,
        }
      }).then(response => {
        this.tableData = response.data.data;
        this.total = response.data.total;
        this.dates = response.data.dates;
        this.museums = response.data.museums;
        this.categories = response.data.categories;
      }).catch(error => {
        console.error(error);
      });
    },
    handleCurrentChange(val) {
      this.currentPage = val;
      this.fetchData();
    },
    //上传图片的方法
    UploadImage(file, fileList) {
      let fd = new FormData();
      fd.append('file', file.raw); // 传给后台接收的名字 file

      axios.post('/api/uploadFile/', fd, {headers: {'Content-Type': 'multipart/form-data'}})
          .then(response => {
            // 上传成功后返回的数据，应该是图片的 URL 字符串
            console.log("上传图片到:" + response.data.imageUrl);
            // 将图片地址给到表单.
            this.form.image = response.data.imageUrl;
          })
          .catch(error => {
            console.error('Error uploading image:', error);
          });
    },

    //移除图片功能
    handleRemove(file, fileList) {
      console.log(file, fileList)

    },
    //预览图片功能
    handlePictureCardPreview(file) {
      console.log(file.url);
      this.dialogVisible = true
      this.dialogImageUrl = file.url
    }
  },
  created() {
    this.fetchData();
  },
}
</script>

<style scoped>
.east-museum-container {
  padding: 20px;
  background-color: #f5f5f5;
}

.el-table {
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
}

.el-table th {
  background-color: #f2f2f2;
  text-align: center;
  font-weight: bold;
}

.el-table td {
  text-align: center;
}

.el-dialog {
  border-radius: 8px;
}

.dialog-form {
  padding: 20px;
}

.dialog-footer {
  text-align: right;
  padding: 10px 20px;
}

.el-button {
  margin-right: 10px;
}

.avatar-uploader {
  display: inline-block;
  width: 178px;
  height: 178px;
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}

.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>
