from git import Repo, GitCommandError
class YGit():

    def __init__(self, owner, repo, tmp_dir, branch=''):
        self.owner = owner
        self.repo = repo
        self.tmp_dir = tmp_dir
        self.branch = branch

    def clone(self):
        self.head = Repo.clone_from('git@git.corp.yahoo.com:'+self.owner+'/'+self.repo,self.tmp_dir+"/"+self.repo)
        master = self.head.heads.master
        return str(master.commit)

    def add(self, dir):
        #index = self.head.index
        #index.add(dir)
        self.head.git.add(dir)

    def commit(self,message):
        index = self.head.index
        log = self.head.git.commit(m=message)
        self.head.git.push()
        return log
