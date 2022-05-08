import React from 'react';
import Highcharts from "highcharts/highmaps";
import HighchartsReact from "highcharts-react-official";
import ua_data from "../ua-topo.json";

const Map = ({data}) => {
    const options = {
        chart: {
            map: ua_data
        },

        title: {
            text: ''
        },

        plotOptions:{
            series:{
                point:{
                    events:{
                        click: function(){
                            console.log(this.name);
                        }
                    }
                }
            }
        },

        series: [{
            data: data,
            name: 'Number of news',
            states: {
                hover: {
                    color: '#BADA55'
                }
            },
            dataLabels: {
                enabled: true,
                format: '{point.name}: 5'
            },
        }]
    }
    return (
        <div>
            <HighchartsReact
                highcharts={Highcharts}
                constructorType={'mapChart'}
                options={options}/>
        </div>
    );
};

export default Map;