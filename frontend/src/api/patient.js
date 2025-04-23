import request from '@/utils/request'

// 获取患者列表
export function getPatientList(params) {
  return request({
    url: '/patient',
    method: 'get',
    params
  })
}

// 获取患者详情
export function getPatientDetail(id) {
  return request({
    url: `/patient/${id}`,
    method: 'get'
  })
}

// 新增患者
export function addPatient(data) {
  return request({
    url: '/patient',
    method: 'post',
    data
  })
}

// 更新患者信息
export function updatePatient(id, data) {
  return request({
    url: `/patient/${id}`,
    method: 'put',
    data
  })
}

// 删除患者
export function deletePatient(id) {
  return request({
    url: `/patient/${id}`,
    method: 'delete'
  })
} 