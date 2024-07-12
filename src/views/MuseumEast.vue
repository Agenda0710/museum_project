<template>
  <div>

    <div class="east-museum-container">
      <el-table :data="tableData" style="width: 100%">
        <el-table-column prop="name" label="文物名称" width="150"></el-table-column>
        <el-table-column prop="category" label="分类" width="150"></el-table-column>
        <el-table-column prop="image" label="图片" width="180">
          <template slot-scope="scope">
            <el-image
                style="width: 100px; height: 100px"
                :src="scope.row.image"
            ></el-image>
          </template>
        </el-table-column>
        <el-table-column prop="date" label="年代" width="150"></el-table-column>
        <el-table-column prop="location" label="位置" width="150"></el-table-column>
        <el-table-column prop="status" label="状态" width="150">
          <template slot-scope="scope">
            <span>{{ scope.row.status === 1 ? '展出' : '未展出' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template slot-scope="scope">
            <el-button @click="handleEdit(scope.row)" type="primary" size="small">修改</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="block">
        <el-pagination
            @current-change="handleCurrentChange"
            :current-page="currentPage"
            :page-size="pageSize"
            :total="total">
        </el-pagination>
      </div>

      <el-dialog :visible.sync="dialogVisible" title="修改文物信息" width="500px">
        <el-form :model="form" label-width="100px" class="dialog-form">
          <el-form-item label="文物名称">
            <el-input v-model="form.name"></el-input>
          </el-form-item>
          <el-form-item label="分类">
            <el-input v-model="form.category"></el-input>
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
          <el-button type="primary" @click="submitForm">提交</el-button>
        </div>
      </el-dialog>
    </div>
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
      form: {
        name: '',
        category: '',
        image: '',
        date: '',
        location: '',
        status: '',
      },
      fileList: [], // 用于存储上传的文件
      editingIndex: -1
    };
  },
  methods: {
    handleEdit(row) {
      this.dialogVisible = true;
      this.form = {...row};
      this.fileList = row.image ? [{name: 'image', url: row.image}] : [];
      this.editingIndex = this.tableData.indexOf(row);
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
          museum_id: 1,
        }
      }).then(response => {
        this.tableData = response.data.data;
        this.total = response.data.total;
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
