<template>
  <div class="department-list">
    <div class="page-header">
      <h2>科室管理</h2>
      <el-button type="primary" @click="$router.push('/departments/add')">新增科室</el-button>
    </div>
    
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="科室名称">
          <el-input v-model="searchForm.DeptName" placeholder="请输入科室名称" clearable />
        </el-form-item>
        <el-form-item label="位置">
          <el-input v-model="searchForm.Location" placeholder="请输入位置" clearable />
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
        <el-table-column prop="DeptID" label="ID" width="80" align="center" />
        <el-table-column prop="DeptName" label="科室名称" min-width="160" align="center" />
        <el-table-column prop="Location" label="位置" min-width="200" align="center" />
        <el-table-column label="操作" width="200" fixed="right" align="center">
          <template #default="scope">
            <el-button
              type="primary"
              size="small"
              @click="handleEdit(scope.row)"
              >编辑</el-button
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
import { ElMessage } from 'element-plus'
import { getDepartmentList } from '@/api/department'

const router = useRouter()
const loading = ref(false)
const departmentList = ref([])
const filteredDepartmentList = ref([])

// 搜索表单
const searchForm = reactive({
  DeptName: '',
  Location: ''
})

// 分页配置
const pagination = reactive({
  current: 1,
  pageSize: 20,
  total: 0
})

// 获取科室列表
const fetchDepartmentList = async () => {
  loading.value = true
  try {
    const res = await getDepartmentList()
    departmentList.value = res.data.list || res.data
    filteredDepartmentList.value = departmentList.value
    pagination.total = departmentList.value.length
    handleSearch() // 获取数据后立即应用筛选
  } catch (error) {
    console.error('获取科室列表失败:', error)
    ElMessage.error('获取科室列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  // 根据搜索条件筛选数据
  filteredDepartmentList.value = departmentList.value.filter(item => {
    const nameMatch = !searchForm.DeptName || 
      item.DeptName.toLowerCase().includes(searchForm.DeptName.toLowerCase())
    const locationMatch = !searchForm.Location || 
      item.Location.toLowerCase().includes(searchForm.Location.toLowerCase())
    return nameMatch && locationMatch
  })
  
  // 更新分页信息
  pagination.total = filteredDepartmentList.value.length
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
  return filteredDepartmentList.value.slice(start, end)
}

// 编辑科室
const handleEdit = (row) => {
  router.push(`/departments/edit/${row.DeptID}`)
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
})
</script>

<style scoped>
.department-list {
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