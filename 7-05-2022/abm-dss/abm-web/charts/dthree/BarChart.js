function useResizeObserver (){

    const {ref, reactive, onMounted, onBeforeUnmount} = Vue
    // create a new ref, 
    // which needs to be attached to an element in a template
    const resizeRef = ref();
    const resizeState = reactive({
      dimensions: {}
    });
  
    const observer = new ResizeObserver(entries => {
      // called initially and on resize
      entries.forEach(entry => {
        resizeState.dimensions = entry.contentRect;
      });
    });
  
    onMounted(() => {
      // set initial dimensions right before observing: Element.getBoundingClientRect()
      resizeState.dimensions = resizeRef.value.getBoundingClientRect();
      observer.observe(resizeRef.value);
    });
  
    onBeforeUnmount(() => {
      observer.unobserve(resizeRef.value);
    });
  
    // return to make them available to whoever consumes this hook
    return { resizeState, resizeRef };
};

export default{
    name: 'Bar',
    setup(){
        const {ref, onMounted, watchEffect}     = Vue
        const {select, scaleLinear, axisBottom, scaleBand}  = d3
        
        const svgRef                   = ref(null)
        //const {resizeRef, resizeState} = useResizeObserver();

        const margin = {top: 20, right: 30, bottom: 40, left: 90}
        const width  = 460 - margin.left - margin.right
        const height = 400 - margin.top - margin.bottom



        let svg
        onMounted(() => {
            svg = select(svgRef.value);
        
            svg
              .attr("width", width + margin.left + margin.right)
              .attr("height", height + margin.top + margin.bottom)

            const x = scaleLinear()
              .domain([0, 100])     //input values  
              .range([ 0, width]);  //full width range
            svg.append("g")
              .attr("transform", "translate(0," + height + ")")
              .call(axisBottom(x))
              .selectAll("text")
                .attr("transform", "translate(-10,0)rotate(-45)")
                .style("text-anchor", "end");

            const y = scaleBand()
              .range([ 0, height ])
              .domain([0,width])
              .padding(.1);
            svg.append("g")
               .call(d3.axisLeft(y))
               
        })

    


        return{
            svgRef
        }

    },

    template:
    `   
        <div ref = resizeRef style = "display: flex">   
            <svg ref = "svgRef"></svg>
        </div> 

    `
}