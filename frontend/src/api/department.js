import request from '@/utils/request'

// 获取科室列表
export function getDepartmentList(params) {
  return request({
    url: '/department',
    method: 'get',
    params
  })
}

// 获取单个科室详情
export function getDepartmentDetail(id) {
  return request({
    url: `/department/${id}`,
    method: 'get'
  })
}

// 新增科室
export function addDepartment(data) {
  return request({
    url: '/department',
    method: 'post',
    data
  })
}

// 更新科室信息
export function updateDepartment(id, data) {
  return request({
    url: `/department/${id}`,
    method: 'put',
    data
  })
}

// 删除科室
export function deleteDepartment(id) {
  return request({
    url: `/department/${id}`,
    method: 'delete'
  })
}