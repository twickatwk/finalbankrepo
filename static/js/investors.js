var allProjects = null

function dataCallback(data) {
    // This function sets the value of allProjects variable
    allProjects = data
    // This function returns the value into the console, for verification
    console.log(allProjects["DeepMind"])
}

function sayHello(amount, projectid) {
    var url = '/addFunds?amount=' + amount + '&pid=' + projectid
    fetch(url).then(function() {
    // Handle response you get from the server
        console.log("Fund is successfully added")
    });
    alert("Fund is successfully added to the project!")
}

class Page extends React.Component {
    render() {

        return(
            <div>
                <MainTitle />
                <ProjectRow />
            </div>
            
        )
    }
}

class Navigator extends React.Component {
    render() {
        return(
            <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
                <a id="nametxt" class="navbar-brand" href="#">The Bank We Need <span id="nametxt2">by DZAC</span></a>
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav">
                        <li class="nav-item active">
                            <a id="linktxt" class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
                        </li>
                        <li class="nav-item">
                            <a id="linktxt" class="nav-link" href="#">My Vault</a>
                        </li>
                    </ul>
                </div>
            </nav>
        )
    }
}

class MainTitle extends React.Component {
    render() {
        return(
            <div class="row">
                <div class="col-12">
                    <h3 id="title">Projects</h3>
                    <p id="title">Support the local youths, and fund their startups today</p>
                </div>
            </div>
        )
    }
}

class ProjectRow extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            values: [],
        };
    }
    // componentDidMount() happens after render()
    componentDidMount() {
        // Use fetch to make an API call to the flask endpoint to retrieve for display
        fetch('./getProjects')
        .then(response => {
            return response.json()
        })
        .then(data => {
            dataCallback(data)
            var names = []
            for (var key in data) {
                names.push(data[key][0]);
            }
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
            data.push(values[key][0])
            data.push(values[key][1])
            data.push(values[key][2])
            rows.push(<ProjectBox data={data}/>)
            data = []
        }

        return(
            <div class="container">
                <div class="row align-items-center">
                    <div class="col-12 d-flex justify-content-center">
                       <ul>
                           {rows}
                        </ul>
                    </div>
                </div>
            </div>
        )
    }
}

class ProjectBox extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            value: this.props.data[0]
        }
        this.addFund = this.addFund.bind(this)
    }
    addFund(event) {
        this.setState({value: event.target.value});
    }

    render(){
        return(
            <div class="card text-white mb-3 bg-light shadow-lg">
                <div class="card-header">{this.props.data[0]}</div>
                <div class="card-body">
                    <h5 class="card-title">{this.props.data[1]}</h5>
                    <p class="card-text">{this.props.data[2]}</p>
                    <div class="row">
                        <div class="col-2">
                            <p><span id="bartxt">Funding Goal:</span></p>
                        </div>
                        <div class="col-10">
                        <div class="progress">
                            <div class="progress-bar" role="progressbar" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100">25%</div>
                            </div>
                        </div>
                    </div>
                    <br/>
                    <form>
                        <div class="form-group">
                            <div class="row">
                                <div class="col-5">
                                    <input onChange={this.addFund} id="amountInput" class="form-control" type="text" placeholder="Enter SGD Amount"/>
                                </div>
                                <div class="col-7">
                                    <div class="btn btn-dark" onClick={() => sayHello(this.state.value, this.props.data[0])}>Fund this Project</div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        )
    }
}

ReactDOM.render(
    <Page />,
    document.getElementById('root')
);