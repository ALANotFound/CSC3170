<template>
  <div class="patient-list">
    <div class="page-header">
      <h2>患者管理</h2>
      <el-button type="primary" @click="$router.push('/patients/add')">新增患者</el-button>
    </div>
    
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="患者姓名">
          <el-input v-model="searchForm.surname" placeholder="请输入患者姓名" clearable />
        </el-form-item>
        <el-form-item label="手机号码">
          <el-input v-model="searchForm.phone" placeholder="请输入手机号码" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-card class="table-card">
      <el-table
        v-loading="loading"
        :data="patientList"
        border
        style="width: 100%"
        :header-cell-style="{textAlign: 'center'}"
        :cell-style="{textAlign: 'center'}"
      >
        <el-table-column prop="PatientID" label="ID" width="80" align="center" />
        <el-table-column prop="Name" label="姓名" min-width="120" align="center" />
        <el-table-column prop="Gender" label="性别" width="80" align="center" />
        <el-table-column label="年龄" width="80" align="center">
          <template #default="scope">
            {{ calculateAge(scope.row.BirthDate) }}
          </template>
        </el-table-column>
        <el-table-column prop="BirthDate" label="出生日期" width="120" align="center" />
        <el-table-column prop="Phone" label="联系电话" min-width="150" align="center" />
        <el-table-column label="操作" width="200" fixed="right" align="center">
          <template #default="scope">
            <el-button
              type="primary"
              size="small"
              @click="handleEdit(scope.row)"
              >编辑</el-button
            >
            <el-button
              type="danger"
              size="small"
              @click="handleDelete(scope.row)"
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.current"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getPatientList, deletePatient } from '@/api/patient'

const router = useRouter()
const loading = ref(false)
const patientList = ref([])

// 搜索表单
const searchForm = reactive({
  surname: '',
  phone: ''
})

// 分页配置
const pagination = reactive({
  current: 1,
  pageSize: 20,
  total: 0
})

// 计算年龄
const calculateAge = (birthDate) => {
  if (!birthDate) return '未知';
  
  const today = new Date();
  const birth = new Date(birthDate);
  let age = today.getFullYear() - birth.getFullYear();
  const monthDiff = today.getMonth() - birth.getMonth();
  
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
    age--;
  }
  
  return age >= 0 ? age : '未知';
}

// 获取患者列表
const fetchPatientList = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.current,
      pageSize: pagination.pageSize,
      ...searchForm
    }
    
    const res = await getPatientList(params)
    patientList.value = res.data.list
    pagination.total = res.data.total
    pagination.current = res.data.page
    pagination.pageSize = res.data.pageSize
  } catch (error) {
    console.error('获取患者列表失败:', error)
    ElMessage.error('获取患者列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.current = 1
  fetchPatientList()
}

// 重置搜索
const resetSearch = () => {
  Object.keys(searchForm).forEach(key => {
    searchForm[key] = ''
  })
  pagination.current = 1
  fetchPatientList()
}

// 编辑患者
const handleEdit = (row) => {
  router.push(`/patients/edit/${row.PatientID}`)
}

// 删除患者
const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除患者 ${row.Name} 吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deletePatient(row.PatientID)
      ElMessage.success('删除成功')
      fetchPatientList()
    } catch (error) {
      console.error('删除患者失败:', error)
      ElMessage.error('删除患者失败')
    }
  }).catch(() => {
    // 取消删除
  })
}

// 页面大小变化
const handleSizeChange = (size) => {
  pagination.pageSize = size
  fetchPatientList()
}

// 当前页变化
const handleCurrentChange = (page) => {
  pagination.current = page
  fetchPatientList()
}

// 组件挂载时获取数据
onMounted(() => {
  fetchPatientList()
})
</script>

<style scoped>
.patient-list {
  width: 100%;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-card {
  margin-bottom: 20px;
}

.table-card {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style> 