# 研究类 Skill 的可移植运行说明

使用你自己安装的 Python 3.10+（macOS / Linux 可用 python3），在目标技能目录解析脚本路径。原入口中发布者的专用虚拟环境不随包提供，也不是必须使用的绝对路径。

优先按技能目录内的 requirements.txt / pyproject.toml 安装对应依赖。论文检索常用 requests、openreview-py、scholarly；网络和图谱常用 networkx、numpy、scipy、pandas、matplotlib、plotly、pyvis、python-louvain；地理数据按需使用 geopandas、shapely、pyproj、pyogrio、pyarrow、folium；OpenAlex 工具按需安装 polite-http、python-dotenv；PDF 输入按实际操作配置 PDF 库。不要为一次任务无差别安装所有包。

文献计量需要 R 和 bibliometrix；Graphviz、jq 仅在对应路线需要。使用自己环境中的 python / Rscript / dot / jq，替换旧平台示例路径。

ORCID_ACCESS_TOKEN、OPENALEX_API_KEY 等由使用者自行设置；ZIP 不含凭据、发布者虚拟环境或私有数据。宿主的检索、联网与绘图能力仍受其工具实际可用范围限制。
