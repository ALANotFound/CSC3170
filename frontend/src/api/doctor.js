import request from '@/utils/request'

// 获取医师列表
export function getDoctorList(params) {
  return request({
    url: '/doctor',
    method: 'get',
    params
  })
}

// 获取医师详情
export function getDoctorDetail(id) {
  return request({
    url: `/doctor/${id}`,
    method: 'get'
  })
}

// 新增医师
export function addDoctor(data) {
  return request({
    url: '/doctor',
    method: 'post',
    data
  })
}

// 更新医师信息
export function updateDoctor(id, data) {
  return request({
    url: `/doctor/${id}`,
    method: 'put',
    data
  })
}

// 删除医师
export function deleteDoctor(id) {
  return request({
    url: `/doctor/${id}`,
    method: 'delete'
  })
} 