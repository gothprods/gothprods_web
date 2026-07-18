const analytics_data = [{"section_times": "{\"home\": 1, \"banda-eventos-semana\": 1}"}, {"section_times": "{}"}, {"section_times": "{\"home\": 4}"}];
const sectionTimeSums = {};
const sectionTimeCounts = {};

analytics_data.forEach(row => {
    try {
        const secTimes = JSON.parse(row.section_times || '{}');
        for (let sec in secTimes) {
            if (secTimes[sec] > 0) {
                let cappedSecTime = Math.min(secTimes[sec], 3600);
                sectionTimeSums[sec] = (sectionTimeSums[sec] || 0) + cappedSecTime;
                sectionTimeCounts[sec] = (sectionTimeCounts[sec] || 0) + 1;
            }
        }
    } catch(e) { console.error(e); }
});

const sectionLabels = Object.keys(sectionTimeSums).map(id => id.replace(/-/g, ' ').toUpperCase());
const sectionData = Object.keys(sectionTimeSums).map(id => Math.round(sectionTimeSums[id] / sectionTimeCounts[id]));

console.log("Labels:", sectionLabels);
console.log("Data:", sectionData);
