<template>
  <div class="ward-list">
    <div class="page-header">
      <h2>病房管理</h2>
      <el-button type="primary" @click="$router.push('/wards/add')">新增病房</el-button>
    </div>
    
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="病房名称">
          <el-input v-model="searchForm.WardName" placeholder="请输入病房名称" clearable />
        </el-form-item>
        <el-form-item label="所属科室">
          <el-select 
            v-model="searchForm.DeptID" 
            placeholder="请选择科室" 
            clearable
            style="width: 200px"
          >
            <el-option 
              v-for="dept in departmentList" 
              :key="dept.DeptID" 
              :label="dept.DeptName" 
              :value="dept.DeptID"
            />
          </el-select>
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
        <el-table-column prop="WardID" label="ID" width="80" align="center" />
        <el-table-column prop="WardName" label="病房名称" min-width="120" align="center" />
        <el-table-column label="所属科室" min-width="150" align="center">
          <template #default="scope">
            {{ getDepartmentName(scope.row.DeptID) }}
          </template>
        </el-table-column>
        <el-table-column prop="Capacity" label="床位数" width="100" align="center" />
        <el-table-column prop="Floor" label="楼层" width="100" align="center" />
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
import { ElMessage, ElMessageBox } from 'element-plus'
import { getWardList, deleteWard } from '@/api/ward'
import { getDepartmentList } from '@/api/department'

const router = useRouter()
const loading = ref(false)
const wardList = ref([])
const filteredWardList = ref([])
const departmentList = ref([])

// 搜索表单
const searchForm = reactive({
  WardName: '',
  DeptID: ''
})

// 分页配置
const pagination = reactive({
  current: 1,
  pageSize: 20,
  total: 0
})

// 获取病房列表
const fetchWardList = async () => {
  loading.value = true
  try {
    const res = await getWardList()
    wardList.value = res.data.list || res.data
    filteredWardList.value = wardList.value
    pagination.total = wardList.value.length
    handleSearch() // 获取数据后立即应用筛选
  } catch (error) {
    console.error('获取病房列表失败:', error)
    ElMessage.error('获取病房列表失败')
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
  filteredWardList.value = wardList.value.filter(item => {
    const nameMatch = !searchForm.WardName || 
      item.WardName.toLowerCase().includes(searchForm.WardName.toLowerCase())
    const deptMatch = !searchForm.DeptID || 
      item.DeptID === searchForm.DeptID
    return nameMatch && deptMatch
  })
  
  // 更新分页信息
  pagination.total = filteredWardList.value.length
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
  return filteredWardList.value.slice(start, end)
}

// 编辑病房
const handleEdit = (row) => {
  router.push(`/wards/edit/${row.WardID}`)
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
  fetchWardList()
})
</script>

<style scoped>
.ward-list {
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