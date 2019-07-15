# Design Document for git-land App

#### User Story
1) As a User <br>
    -   As a programmer, I should be able to add my SSH key 
    -   As a programmer, I should be able to create a repo
    -   As a programmer, I should be able to push my local changes to the remote GitLab repo through SSH
    -   As a programmer, I should be able to view all the files in my repo on the website
    -   As a programmer, I should be able to run all my test cases when I push changes to a branch and see the status of the test cases



#### MVP
1) User Registration/ Login and include user's public ssh key also
2) Create Repository
3) Setup SSH Connection
4) File transfer between local ad remote
5) Basic UI for displaying folder -  Code Highlighting, README.md markdown parser
6) CI using Docker

#### URL Design <br>

-   `/` or `/<username>` : List of all User Repos
-   `/login` : Login page(Displayed whenuser is not looged in)
-   `/register` : Resgistration Page
-   `/repo/create`: Create Repository  
-   `/username/<repo_name>` : Repo View
-   `/username/<repo_name>/<filepath>` :Open File
-   `/username/<repo_name>/delete` : DeleteConfirmation Page 
-   `/profile/username` : Profile
-   `/profile/edit` : Edit Account
    


#### Forms
    -   SignUp : {
            Username : string,
            email : EmailField,
            ssh key : string,
            password: string,
        } 

    -   Login : {
            username/email: string,
            password: string
        }  

    -   CreateRepo : {
            Repo Name : String
        }
    -   EditAccount : {
            ssh key : string,
            password: string,
        }
    

####    Authentication
    * Any registered user can create a repo

#### Database Schema Design

    -   Ssh_key : {
                "ssh_name" : string;
                "ssh_key" : string;
                "user" : ForiegnKey(related field='keys')
    }
    -   Repository : {
                    name : string,
                    username : ForeignKey(User),
                    repo_path : FileField(),
                    create_time : time,
                    last_update : time,
            }

    -   Test_info : {
                    commit_id : string,
                    commit_message: string,
                    Repo : ForeignKey(repository)
                    test_exit_code: IntegerField(),
                    log : string
                }            





