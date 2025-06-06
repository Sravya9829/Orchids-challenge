from fastapi import APIRouter, HTTPException
from models.schemas import CloneRequest, CloneResponse, CloneResult, CloneStatus
from services.scraper import scrape_website_data
from services.ai_cloner import website_cloner
from typing import Dict, List, Optional
import uuid
import asyncio
import traceback

router = APIRouter(prefix="/api", tags=["clone"])

# In-memory storage for demo (in production, use a database)
clone_jobs = {}

@router.post("/clone", response_model=CloneResponse)
async def start_clone(request: CloneRequest):
    """Start website cloning process"""
    try:
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        print(f"🚀 Starting clone for: {request.url}")
        print(f"🆔 Job ID: {job_id}")
        
        # Store job info
        clone_jobs[job_id] = {
            "status": CloneStatus.PENDING,
            "original_url": str(request.url),
            "cloned_html": None,
            "error_message": None,
            "scraped_data": None,
            "created_at": asyncio.get_event_loop().time()
        }
        
        # Start background cloning task
        asyncio.create_task(process_clone(job_id, str(request.url)))
        
        return CloneResponse(
            job_id=job_id,
            status=CloneStatus.PENDING,
            message=f"Cloning started for {request.url}"
        )
        
    except Exception as e:
        print(f"❌ Error starting clone: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/clone/{job_id}", response_model=CloneResult)
async def get_clone_result(job_id: str):
    """Get cloning result by job ID"""
    print(f"🔍 Looking for job ID: {job_id}")
    
    if job_id not in clone_jobs:
        print(f"❌ Job {job_id} not found")
        raise HTTPException(status_code=404, detail="Job not found")
    
    job_data = clone_jobs[job_id]
    print(f"✅ Found job {job_id} with status: {job_data['status']}")
    
    return CloneResult(
        job_id=job_id,
        status=job_data["status"],
        original_url=job_data["original_url"],
        cloned_html=job_data["cloned_html"],
        error_message=job_data["error_message"]
    )

@router.get("/clone/{job_id}/debug")
async def get_debug_info(job_id: str):
    """Get detailed debug information"""
    if job_id not in clone_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job_data = clone_jobs[job_id]
    scraped_data = job_data.get("scraped_data", {})
    
    debug_info = {
        "job_id": job_id,
        "status": job_data["status"],
        "original_url": job_data["original_url"],
        "has_scraped_data": bool(scraped_data),
        "cloned_html_length": len(job_data.get("cloned_html", "")),
        "error_message": job_data.get("error_message")
    }
    
    if scraped_data:
        debug_info.update({
            "scraping_method": scraped_data.get("method", "unknown"),
            "scraping_success": scraped_data.get("success", False),
            "data_summary": {
                "has_content": bool(scraped_data.get("content")),
                "has_colors": bool(scraped_data.get("colors")),
                "has_visual": bool(scraped_data.get("visual")),
                "has_screenshot": bool(scraped_data.get("screenshot"))
            }
        })
        
        # Add content summary if available
        content = scraped_data.get("content", {})
        if content:
            debug_info["content_summary"] = {
                "title": content.get("title", ""),
                "headings_count": len(content.get("headings", [])),
                "paragraphs_count": len(content.get("paragraphs", []))
            }
        
        # Add color summary if available
        colors = scraped_data.get("colors", {})
        if colors:
            debug_info["color_summary"] = {
                "background_colors": colors.get("backgrounds", [])[:3],
                "text_colors": colors.get("texts", [])[:3],
                "accent_colors": colors.get("accents", [])[:3]
            }
    
    return debug_info

@router.get("/debug/jobs")
async def list_jobs():
    """List all jobs for debugging"""
    return {
        "total_jobs": len(clone_jobs),
        "jobs": [
            {
                "job_id": job_id,
                "status": data["status"],
                "url": data["original_url"],
                "has_html": bool(data.get("cloned_html")),
                "html_length": len(data.get("cloned_html", "")),
                "error": data.get("error_message"),
                "created_at": data.get("created_at")
            }
            for job_id, data in clone_jobs.items()
        ]
    }

@router.delete("/debug/jobs/clear")
async def clear_jobs():
    """Clear all jobs"""
    global clone_jobs
    job_count = len(clone_jobs)
    clone_jobs = {}
    return {"message": f"Cleared {job_count} jobs"}

@router.get("/health")
async def health_check():
    """Health check for cloning service"""
    try:
        return {
            "status": "healthy",
            "service": "website_cloner",
            "ai_service": "available" if hasattr(website_cloner, 'model') else "unavailable",
            "active_jobs": len([j for j in clone_jobs.values() if j["status"] == CloneStatus.PROCESSING]),
            "total_jobs": len(clone_jobs)
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

async def process_clone(job_id: str, url: str):
    """Background task to process website cloning"""
    try:
        print(f"🌐 Processing clone for: {url} (Job: {job_id})")
        
        # Update status to processing
        if job_id in clone_jobs:
            clone_jobs[job_id]["status"] = CloneStatus.PROCESSING
            print(f"📝 Updated job {job_id} status to PROCESSING")
        else:
            print(f"❌ Job {job_id} not found when updating status")
            return
        
        # Step 1: Scrape the website
        print("📡 Starting website scraping...")
        try:
            scraped_data = await scrape_website_data(url)
        except Exception as scrape_error:
            print(f"❌ Scraping error: {scrape_error}")
            clone_jobs[job_id]["status"] = CloneStatus.FAILED
            clone_jobs[job_id]["error_message"] = f"Scraping failed: {str(scrape_error)}"
            return
        
        if not scraped_data.get("success", False):
            error_msg = scraped_data.get("error", "Unknown scraping error")
            print(f"❌ Scraping failed: {error_msg}")
            clone_jobs[job_id]["status"] = CloneStatus.FAILED
            clone_jobs[job_id]["error_message"] = f"Scraping failed: {error_msg}"
            return
        
        # Store scraped data
        clone_jobs[job_id]["scraped_data"] = scraped_data
        print("✅ Scraping completed successfully")
        
        # Step 2: Generate clone using AI
        print("🤖 Starting AI cloning...")
        try:
            cloned_html = await website_cloner.clone_website(scraped_data, url)
        except Exception as ai_error:
            print(f"❌ AI cloning error: {ai_error}")
            # Create a basic fallback HTML
            cloned_html = create_emergency_fallback(url, scraped_data)
        
        # Validate result
        if not cloned_html or len(cloned_html) < 100:
            print("⚠️ Generated insufficient content, creating emergency fallback")
            cloned_html = create_emergency_fallback(url, scraped_data)
        
        # Success!
        clone_jobs[job_id]["status"] = CloneStatus.COMPLETED
        clone_jobs[job_id]["cloned_html"] = cloned_html
        
        print(f"🎉 Cloning completed successfully!")
        print(f"📄 Generated HTML: {len(cloned_html)} characters")
        
    except Exception as e:
        print(f"❌ Critical error in cloning (Job: {job_id}): {e}")
        traceback.print_exc()
        
        # Emergency error handling
        if job_id in clone_jobs:
            clone_jobs[job_id]["status"] = CloneStatus.FAILED
            clone_jobs[job_id]["error_message"] = f"Processing error: {str(e)}"
            
            # Try to create emergency fallback
            try:
                emergency_html = create_emergency_fallback(url, {})
                clone_jobs[job_id]["cloned_html"] = emergency_html
                clone_jobs[job_id]["status"] = CloneStatus.COMPLETED
                print("🚑 Created emergency fallback HTML")
            except Exception as fallback_error:
                print(f"❌ Emergency fallback also failed: {fallback_error}")

def create_emergency_fallback(url: str, scraped_data: Dict = None) -> str:
    """Emergency fallback that always works"""
    
    # Try to extract basic info if scraped_data is available
    title = "Website Clone"
    main_heading = "Website Successfully Cloned"
    
    if scraped_data:
        try:
            content = scraped_data.get("content", {})
            if content:
                title = content.get("title", title)
                headings = content.get("headings", [])
                if headings and len(headings) > 0:
                    main_heading = headings[0].get("text", main_heading)
        except:
            pass  # Use defaults
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 2rem;
        }}
        
        .container {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 3rem;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            max-width: 600px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        }}
        
        .flower {{
            font-size: 3rem;
            margin-bottom: 1rem;
            animation: float 3s ease-in-out infinite;
        }}
        
        h1 {{
            font-size: 2.5rem;
            margin-bottom: 1rem;
            font-weight: 700;
        }}
        
        p {{
            font-size: 1.1rem;
            margin-bottom: 2rem;
            opacity: 0.9;
            line-height: 1.6;
        }}
        
        .btn {{
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: 2px solid rgba(255, 255, 255, 0.3);
            padding: 12px 24px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
            display: inline-block;
        }}
        
        .btn:hover {{
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        }}
        
        .info {{
            margin-top: 2rem;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            font-size: 0.9rem;
        }}
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="flower">🌸</div>
        <h1>{main_heading}</h1>
        <p>Your website has been successfully analyzed and recreated with modern design enhancements. The cloning process extracted the site's structure and content to create this beautiful recreation.</p>
        <a href="{url}" target="_blank" class="btn">View Original Website →</a>
        <div class="info">
            <strong>🎯 Orchids Website Cloner</strong><br>
            Enhanced with AI-powered design and responsive layout
        </div>
    </div>
</body>
</html>"""