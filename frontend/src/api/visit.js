import request from '@/utils/request'

// 获取就诊记录列表
export function getVisitList(params) {
  return request({
    url: '/visit',
    method: 'get',
    params
  })
}

// 获取就诊记录详情
export function getVisitDetail(id) {
  return request({
    url: `/visit/${id}`,
    method: 'get'
  })
}

// 新增就诊记录
export function addVisit(data) {
  return request({
    url: '/visit',
    method: 'post',
    data
  })
}

// 更新处方
export function updatePrescription(id, data) {
  return request({
    url: `/visit/${id}/prescription`,
    method: 'put',
    data
  })
}

// 删除就诊记录
export function deleteVisit(id) {
  return request({
    url: `/visit/${id}`,
    method: 'delete'
  })
} 