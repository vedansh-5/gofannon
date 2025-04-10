module.exports = async ({github, context}) => {  
  // Get the draft release  
  const { data: release } = await github.rest.repos.getRelease({  
    owner: context.repo.owner,  
    repo: context.repo.repo,  
    release_id: process.env.RELEASE_ID  
  });  
    
  // Publish the release  
  await github.rest.repos.updateRelease({  
    owner: context.repo.owner,  
    repo: context.repo.repo,  
    release_id: process.env.RELEASE_ID,  
    draft: false,  
    name: release.name,  
    tag_name: release.tag_name,  
    body: release.body  
  });  
    
  console.log(`Published release ${release.name}`);  
};  
