import streamlit as st
import pandas as pd


def segmentation_ui():
    st.markdown("### 🗂️ Segmentation Simulation")

    st.info(
        "**How it works:** Enter base addresses and limits for each segment. "
        "Logical addresses are expressed as `segment,offset` pairs. "
        "The simulator translates them to physical addresses and detects faults.",
        icon="ℹ️",
    )

    col1, col2 = st.columns(2)

    with col1:
        base_input  = st.text_input(
            "Base Addresses (space-separated, one per segment)",
            value="1000 2000 3000",
            help="Starting physical address of each segment"
        )
        limit_input = st.text_input(
            "Limits (space-separated, one per segment)",
            value="400 500 600",
            help="Maximum offset allowed in each segment"
        )

    with col2:
        addr_input = st.text_area(
            "Logical Addresses (format: seg,offset — one per line or space-separated)",
            value="0,200\n1,450\n2,700\n1,499\n3,100",
            height=140,
            help="Example: '0,200' means segment 0, offset 200"
        )

    if st.button("🔄 Translate Addresses", use_container_width=True):
        try:
            base_list  = list(map(int, base_input.split()))
            limit_list = list(map(int, limit_input.split()))

            if len(base_list) != len(limit_list):
                st.error("Number of base addresses must equal number of limits.")
                return

            # Accept both newline and space-separated pairs
            raw_pairs = addr_input.replace("\n", " ").split()
            results   = []

            for pair in raw_pairs:
                if "," not in pair:
                    st.warning(f"Skipping invalid entry `{pair}` — expected format: seg,offset")
                    continue

                try:
                    seg, offset = map(int, pair.split(","))
                except ValueError:
                    st.warning(f"Skipping `{pair}` — values must be integers.")
                    continue

                if seg >= len(base_list):
                    results.append({
                        "Logical (seg, offset)": pair,
                        "Segment":  seg,
                        "Offset":   offset,
                        "Base":     "—",
                        "Limit":    "—",
                        "Physical": "—",
                        "Status":   "❌ Segment Not Found",
                    })
                elif offset >= limit_list[seg]:
                    results.append({
                        "Logical (seg, offset)": pair,
                        "Segment":  seg,
                        "Offset":   offset,
                        "Base":     base_list[seg],
                        "Limit":    limit_list[seg],
                        "Physical": "—",
                        "Status":   "❌ Segmentation Fault (offset ≥ limit)",
                    })
                else:
                    physical = base_list[seg] + offset
                    results.append({
                        "Logical (seg, offset)": pair,
                        "Segment":  seg,
                        "Offset":   offset,
                        "Base":     base_list[seg],
                        "Limit":    limit_list[seg],
                        "Physical": physical,
                        "Status":   "✅ Valid",
                    })

            if results:
                df = pd.DataFrame(results)
                st.markdown("#### 📋 Translation Results")
                st.dataframe(df, use_container_width=True)

                valid   = sum(1 for r in results if "Valid" in r["Status"])
                faults  = len(results) - valid

                m1, m2, m3 = st.columns(3)
                m1.metric("Total Accesses", len(results))
                m2.metric("✅ Valid",        valid)
                m3.metric("❌ Faults",       faults)

                # Segment table summary
                st.markdown("#### 🗺️ Segment Table")
                seg_data = [
                    {"Segment": i, "Base": base_list[i], "Limit": limit_list[i],
                     "Range": f"{base_list[i]} – {base_list[i] + limit_list[i] - 1}"}
                    for i in range(len(base_list))
                ]
                st.table(pd.DataFrame(seg_data))

        except ValueError as e:
            st.error(f"Input error: {e}")
