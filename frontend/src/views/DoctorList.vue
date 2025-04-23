<template>
  <div class="doctor-list">
    <div class="page-header">
      <h2>医师管理</h2>
      <el-button type="primary" @click="$router.push('/doctors/add')">新增医师</el-button>
    </div>
    
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="医师姓名">
          <el-input v-model="searchForm.Name" placeholder="请输入医师姓名" clearable />
        </el-form-item>
        <el-form-item label="科室">
          <el-select 
            v-model="searchForm.DeptID" 
            placeholder="请选择科室" 
            clearable
            style="width: 200px"
            filterable
          >
            <el-option 
              v-for="dept in departmentList" 
              :key="dept.DeptID" 
              :label="dept.DeptName" 
              :value="dept.DeptID" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="职称">
          <el-input v-model="searchForm.Title" placeholder="请输入职称" clearable />
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
        :data="getCurrentPageData()"
        border
        style="width: 100%"
        :header-cell-style="{textAlign: 'center'}"
        :cell-style="{textAlign: 'center'}"
      >
        <el-table-column prop="DoctorID" label="ID" width="80" align="center" />
        <el-table-column prop="Name" label="姓名" min-width="120" align="center" />
        <el-table-column label="科室" min-width="150" align="center">
          <template #default="scope">
            {{ getDepartmentName(scope.row.DeptID) }}
          </template>
        </el-table-column>
        <el-table-column prop="Title" label="职称" min-width="150" align="center" />
        <el-table-column prop="Phone" label="联系电话" min-width="150" align="center" />
        <el-table-column prop="createTime" label="创建时间" min-width="180" align="center" />
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
import { getDoctorList, deleteDoctor } from '@/api/doctor'
import { getDepartmentList } from '@/api/department'

const router = useRouter()
const loading = ref(false)
const doctorList = ref([])
const filteredDoctorList = ref([])
const departmentList = ref([])

// 搜索表单
const searchForm = reactive({
  Name: '',
  DeptID: '',
  Title: ''
})

// 分页配置
const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0
})

// 获取医师列表
const fetchDoctorList = async () => {
  loading.value = true
  try {
    const res = await getDoctorList()
    doctorList.value = res.data.list || res.data
    filteredDoctorList.value = doctorList.value
    pagination.total = doctorList.value.length
    handleSearch() // 获取数据后立即应用筛选
  } catch (error) {
    console.error('获取医师列表失败:', error)
    ElMessage.error('获取医师列表失败')
  } finally {
    loading.value = false
  }
}

// 获取科室列表
const fetchDepartmentList = async () => {
  try {
    const res = await getDepartmentList()
    departmentList.value = res.data.list || res.data || []
  } catch (error) {
    console.error('获取科室列表失败:', error)
    ElMessage.error('获取科室列表失败')
    departmentList.value = []
  }
}

// 根据科室ID获取科室名称
const getDepartmentName = (deptId) => {
  if (!deptId) return '未知科室'
  const dept = departmentList.value.find(item => item.DeptID === deptId)
  return dept ? dept.DeptName : '未知科室'
}

// 搜索
const handleSearch = () => {
  // 根据搜索条件筛选数据
  filteredDoctorList.value = doctorList.value.filter(item => {
    const nameMatch = !searchForm.Name || 
      item.Name.toLowerCase().includes(searchForm.Name.toLowerCase())
    const deptMatch = !searchForm.DeptID || 
      item.DeptID === searchForm.DeptID
    const titleMatch = !searchForm.Title || 
      item.Title.toLowerCase().includes(searchForm.Title.toLowerCase())
    return nameMatch && deptMatch && titleMatch
  })
  
  // 更新分页信息
  pagination.total = filteredDoctorList.value.length
  pagination.current = 1
}

// 重置搜索
const resetSearch = () => {
  Object.keys(searchForm).forEach(key => {
    searchForm[key] = ''
  })
  handleSearch()
}

// 获取当前页的数据
const getCurrentPageData = () => {
  const start = (pagination.current - 1) * pagination.pageSize
  const end = start + pagination.pageSize
  return filteredDoctorList.value.slice(start, end)
}

// 编辑医师
const handleEdit = (row) => {
  router.push(`/doctors/edit/${row.DoctorID}`)
}

// 删除医师
const handleDelete = (row) => {
  ElMessageBox.confirm(
    `确定要删除医师 ${row.Name} 吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteDoctor(row.DoctorID)
      ElMessage.success('删除成功')
      fetchDoctorList()
    } catch (error) {
      // 检查是否是204状态码（删除成功）
      if (error.response && error.response.status === 204) {
        ElMessage.success('删除成功')
        fetchDoctorList()
        return
      }
      console.error('删除医师失败:', error)
      ElMessage.error('删除医师失败')
    }
  }).catch(() => {
    // 取消删除
  })
}

// 页面大小变化
const handleSizeChange = (size) => {
  pagination.pageSize = size
  pagination.current = 1
}

// 当前页变化
const handleCurrentChange = (page) => {
  pagination.current = page
}

// 组件挂载时获取数据
onMounted(() => {
  fetchDepartmentList()
  fetchDoctorList()
})
</script>

<style scoped>
.doctor-list {
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