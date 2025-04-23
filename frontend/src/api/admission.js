import request from '@/utils/request'

// 获取在院患者列表
export function getActiveAdmissions(params) {
  return request({
    url: '/admission/active',
    method: 'get',
    params
  })
}

// 办理入院
export function addAdmission(data) {
  return request({
    url: '/admission',
    method: 'post',
    data
  })
}

// 办理出院
export function dischargePatient(id, data) {
  return request({
    url: `/admission/${id}/discharge`,
    method: 'put',
    headers: {
      'Content-Type': 'application/json'
    },
    data
  })
} 