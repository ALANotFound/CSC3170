import request from '@/utils/request'

// 获取病房列表
export function getWardList(params) {
  return request({
    url: '/ward',
    method: 'get',
    params
  })
}

// 获取病房详情
export function getWardDetail(id) {
  return request({
    url: `/ward/${id}`,
    method: 'get'
  })
}

// 新增病房
export function addWard(data) {
  return request({
    url: '/ward',
    method: 'post',
    data
  })
}

// 更新病房信息
export function updateWard(id, data) {
  return request({
    url: `/ward/${id}`,
    method: 'put',
    data
  })
}

// 删除病房
export function deleteWard(id) {
  return request({
    url: `/ward/${id}`,
    method: 'delete'
  })
} 