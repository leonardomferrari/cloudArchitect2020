const random = require('./random')

const fake = {
  devices: [
    'ptuudlga',
    'ouaurksl',
    'ttzccikk',
    'didebjal',
    'wydjgfqr',
    'zpfjecet',
    'lndbbrwb',
    'gxcyuaau'
  ],
  createData () {
    const deviceId = fake.devices[random.createInteger(0, 7)]
    const data = {
      deviceId,
      device: "device-0",
      group: "group-0",
      devicetype: "FS-15",
      date: "01-04-2018T00:0:00.000Z",
      inputcurrent: Math.floor(850 + Math.random() * 100),
      inputcurrentunit: "amp",
      inputvoltage: Math.floor(210 + Math.random() * 20),
      inputvoltageunit: "ac-v",
      temp1: Math.floor(45 + Math.random() * 10),
      temp1unit: "c",
      temp2: Math.floor(25 + Math.random() * 10),
      temp2unit: "c",
      scale1: Math.floor(35 + Math.random() * 10),
      scale1unit: "kg",
      scale2: Math.floor(12 + Math.random() * 5),
      scale2unit: "kg",
      flow: Math.floor(40 + Math.random() * 10),
      flowunit: "m3/h",
    }
    return data
  }
}

module.exports = fake
