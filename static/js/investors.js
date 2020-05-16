

class Page extends React.Component {
    render() {
        return(
            <div>
                <Navigator />
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
    render() {
        return(
            <div class="container">
                <div class="row">
                    <div class="col-6 d-flex justify-content-center">
                        <ProjectBox />
                    </div>
                    <div class="col-6 d-flex justify-content-center">
                        <ProjectBox />
                    </div>
                </div>
            </div>
        )
    }
}

class ProjectBox extends React.Component {
    render(){
        return(
            <div class="card text-white bg-success mb-3 bg-black shadow-lg">
                <div class="card-header">SpaceX</div>
                <div class="card-body">
                    <h5 class="card-title">Falcon Rocket</h5>
                    <p class="card-text">Falcon 9 is a partially reusable two-stage-to-orbit medium lift launch vehicle designed and manufactured by SpaceX in the United States. It is powered by Merlin engines, also developed by SpaceX, burning cryogenic liquid oxygen and rocket-grade kerosene as propellants.</p>
                    <button type="button" class="btn btn-dark">Fund this Project</button>
                </div>
            </div>
        )
    }
}

ReactDOM.render(
    <Page />,
    document.getElementById('root')
);