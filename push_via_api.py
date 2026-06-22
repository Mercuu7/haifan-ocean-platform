"""
海帆智擎 · API 推送脚本
当 git push 被墙时使用此脚本，通过 GitHub API 上传修改的文件。
用法: python push_via_api.py index.html dashboard.html
"""
import sys, os, json, base64, subprocess

REPO = "Mercuu7/haifan-ocean-platform"
GH_EXE = r"C:\Program Files\GitHub CLI\gh.exe"

def run_gh(*args):
    """Run gh CLI with args, return stdout."""
    result = subprocess.run(
        [GH_EXE] + list(args),
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        print(f"[ERROR] gh {' '.join(args[:2])}: {result.stderr.strip()}")
        return None
    return result.stdout.strip()

def get_remote_sha(path):
    """Get current SHA of a file on GitHub."""
    out = run_gh("api", f"repos/{REPO}/contents/{path}", "--jq", ".sha")
    return out

def push_file(local_path, remote_path, message):
    """Push a single file to GitHub via Contents API."""
    if not os.path.exists(local_path):
        print(f"[SKIP] {local_path} not found")
        return False

    sha = get_remote_sha(remote_path)
    if not sha:
        print(f"[SKIP] Cannot get remote SHA for {remote_path}")
        return False

    with open(local_path, "rb") as f:
        content_b64 = base64.b64encode(f.read()).decode()

    payload = {
        "message": message,
        "content": content_b64,
        "sha": sha,
        "branch": "main"
    }

    # Write payload to temp file (avoids command line length limit)
    tmpfile = os.path.join(os.environ.get("TEMP", "/tmp"), f"gh_push_{os.path.basename(local_path)}.json")
    with open(tmpfile, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)

    out = run_gh("api", f"repos/{REPO}/contents/{remote_path}", "--method", "PUT", "--input", tmpfile, "--jq", ".commit.sha")
    if out:
        print(f"[OK] {remote_path} → commit {out[:7]}")
        return True
    return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python push_via_api.py <file1> [file2] [...]")
        print("Example: python push_via_api.py index.html dashboard.html")
        sys.exit(1)

    message = input("Commit message: ").strip()
    if not message:
        message = "Update website files"

    for local_path in sys.argv[1:]:
        # Use the same path as remote path
        push_file(local_path, local_path, message)

    print("\nDone! GitHub Pages will auto-deploy in 1-2 minutes.")

if __name__ == "__main__":
    main()
