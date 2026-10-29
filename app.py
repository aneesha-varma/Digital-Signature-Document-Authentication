import streamlit as st

from crypto_utils import (
    generate_key_pair,
    sign_document,
    verify_document,
    KEY_DIR
)

from pathlib import Path


st.set_page_config(
    page_title="Document Authentication System",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 Digital Signature-Based Document Authentication")
st.write(
    "Securely sign documents and verify their integrity "
    "using RSA digital signatures and SHA-256."
)

st.info(
    "This is an educational demonstration. "
    "Use test documents, not confidential files."
)

# ---------------- KEY MANAGEMENT ----------------

st.header("1. RSA Key Management")

public_key_path = KEY_DIR / "public_key.pem"
private_key_path = KEY_DIR / "private_key.pem"

if st.button("Generate RSA Key Pair"):
    public_pem = generate_key_pair()
    st.session_state["public_pem"] = public_pem
    st.success("RSA key pair generated successfully.")

if private_key_path.exists() and public_key_path.exists():
    st.success("A local RSA key pair is available.")

    public_pem = public_key_path.read_bytes()

    st.download_button(
        label="Download Public Key",
        data=public_pem,
        file_name="public_key.pem",
        mime="application/x-pem-file"
    )

    st.warning(
        "The private key is stored locally without a password. "
        "Never publish it or use this setup for production."
    )
else:
    st.warning("Generate a key pair before signing documents.")

# ---------------- APPLICATION TABS ----------------

sign_tab, verify_tab = st.tabs(["Sign Document", "Verify Document"])

with sign_tab:
    st.subheader("2. Sign a Document")

    uploaded_document = st.file_uploader(
        "Choose the document to sign",
        key="sign_document"
    )

    if st.button("Sign Document", key="sign_button"):
        if uploaded_document is None:
            st.error("Please upload a document first.")

        elif not private_key_path.exists():
            st.error("Generate an RSA key pair first.")

        else:
            try:
                document_bytes = uploaded_document.getvalue()

                signature_record = sign_document(
                    document_bytes,
                    uploaded_document.name
                )

                st.session_state["signed_record"] = signature_record

                st.success("Document signed successfully!")

                st.download_button(
                    "Download Signature Record",
                    data=signature_record,
                    file_name=uploaded_document.name + ".sig.json",
                    mime="application/json",
                    key="download_signature"
                )

            except Exception as error:
                st.error(f"Signing failed: {error}")

with verify_tab:
    st.subheader("3. Verify a Document")

    document_to_verify = st.file_uploader(
        "Upload the original or received document",
        key="verify_document"
    )

    signature_file = st.file_uploader(
        "Upload its .sig.json signature record",
        type=["json"],
        key="verify_signature"
    )

    public_key_file = st.file_uploader(
        "Upload the signer's public_key.pem",
        type=["pem"],
        key="verify_public_key"
    )

    if st.button("Verify Authenticity"):
        if not all([
            document_to_verify,
            signature_file,
            public_key_file
        ]):
            st.error(
                "Please upload the document, signature record, "
                "and public key."
            )

        else:
            try:
                is_valid, message = verify_document(
                    document_to_verify.getvalue(),
                    signature_file.getvalue(),
                    public_key_file.getvalue()
                )

                if is_valid:
                    st.success("✅ VERIFIED: " + message)
                else:
                    st.error("❌ VERIFICATION FAILED: " + message)

            except Exception as error:
                st.error(f"Verification error: {error}")

st.divider()

st.caption(
    "Cryptography: RSA-PSS | Hashing: SHA-256 | "
    "Interface: Streamlit"
)