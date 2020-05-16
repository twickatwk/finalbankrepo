

class LoanBox extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            values: [],
        };
    }

    componentDidMount() {
        // Use fetch to make an API call to the flask endpoint to retrieve for display
        fetch('./getProjectsByUser')
        .then(response => {
            return response.json()
        })
        .then(data => {
            // alert(data)
            this.setState({ values: data })
            // NOTE: React component generation doesnt work inside the fetch method
            
        })
        .catch(err => {
            // Do something for an error here
            alert("Error occurred")
        })
    }

    render() { 

        const { values } = this.state;

        var rows = []
        var data = []

        for (var key in values) {
            data.push(key)
            // project name
            data.push(values[key][0])
            // project description
            data.push(values[key][1])
            // project goal
            data.push(values[key][2])
            rows.push(<Loan data={data}/>)
            data = []
        }


        return (
            <div class="col-md-12 mar-tb-20 text-center hero-catagory-wrapper v1" >
                   {rows}
            </div>
        )
    }
}

class Loan extends React.Component {
    render() {
        return (
            <a href="#" class="hero-category-content v1">
                    <p class="name">Project Name : {this.props.data[1]}</p>
                    <p class="d-name">
                    {this.props.data[2]}<br/>
                    </p>
            </a>
        )
    }
}


ReactDOM.render(
    <LoanBox />,
    document.getElementById('loansdata')
);