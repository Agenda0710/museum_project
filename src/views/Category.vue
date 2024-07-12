<template>
  <div>
    <template>
      <el-table
          :data="tableData"
          style="width: 100%">
        <el-table-column
            prop="id"
            label="编号"
            width="380">
        </el-table-column>
        <el-table-column
            prop="name"
            label="分类名称"
            width="380">
        </el-table-column>
        <el-table-column label="操作" width="480">
          <template slot-scope="scope">
            <el-button @click="handleEdit(scope.row)" type="primary" size="small">修改</el-button>&nbsp;
            <el-popconfirm
                title="这是一段内容确定删除吗？"
                @confirm="deleteCategory(scope.row)"
            >
              <el-button slot="reference" type="danger" size="small">删除</el-button>
            </el-popconfirm>

          </template>
        </el-table-column>
      </el-table>
    </template>

    <el-dialog :visible.sync="dialogVisible" title="修改分类信息" width="500px">
      <el-form :model="form" label-width="100px" class="dialog-form">
        <el-form-item label="分类名称">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">提交</el-button>
      </div>

    </el-dialog>

  </div>
</template>

<script>
import axios from "axios";

export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "Category",
  data() {
    return {
      dialogVisible: false,
      tableData: [],
      form: {
        name: '',
      }
    }
  },
  methods: {
    handleEdit(row) {
      this.dialogVisible = true;
      this.form = {...row};
      this.editingIndex = this.tableData.indexOf(row);
    },
    fetchData() {
      axios.get("/api/getCategory/").then((response) => {
        this.tableData = response.data;
      })
    },
    deleteCategory(row) {
      axios.delete("/api/deleteCategory/" + row.id + "/").then(() => {
        this.fetchData()
      }).catch(error => {
        console.log(error);
      })
    },
    submitForm() {
      axios.post('/api/updateCategory/', this.form).then(() => {
        this.fetchData();
        this.dialogVisible = false;
      }).catch(error => {
        console.error('Error updating category:', error);
      });
    }
  },
  created() {
    this.fetchData();
  },
}
</script>

<style scoped>

</style>