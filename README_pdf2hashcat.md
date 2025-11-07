# pdf2hashcat - PDF Password Hash Extractor

A pure Bash tool to extract password hashes from encrypted PDF files for use with hashcat.

## Features

- **Pure Bash** - No Python, Perl, or external libraries required
- **Universal PDF support** - Works with all PDF versions:
  - PDF 1.1-1.3 (Acrobat 2-4) - RC4-40 bit encryption
  - PDF 1.4-1.6 (Acrobat 5-8) - RC4-128 bit encryption
  - PDF 1.4-1.6 (Acrobat 5-8) - AES-128 bit encryption
  - PDF 1.7 Extension Level 3 (Acrobat 9-X) - AES-256 bit encryption
  - PDF 1.7 Extension Level 8 (Acrobat XI+) - AES-256 bit encryption
- **Lightweight** - Uses only standard Unix/Linux tools (grep, sed, awk, xxd)
- **Hashcat-ready output** - Formats hashes for direct use with hashcat
- **Verbose mode** - Debug output for troubleshooting

## Requirements

- Bash 4.0 or higher
- Standard Unix tools: grep, awk, xxd, tr, head, cat
- Available by default on virtually all Linux/Unix systems

## Installation

```bash
chmod +x pdf2hashcat.sh
```

## Usage

### Basic Usage

```bash
./pdf2hashcat.sh encrypted_document.pdf
```

### Verbose Mode

```bash
./pdf2hashcat.sh -v encrypted_document.pdf
```

### Save Hash to File

```bash
./pdf2hashcat.sh encrypted_document.pdf > hash.txt
```

### Help

```bash
./pdf2hashcat.sh -h
```

## Using with Hashcat

After extracting the hash, use it with hashcat:

### PDF 1.1-1.3 (RC4-40)
```bash
./pdf2hashcat.sh document.pdf > hash.txt
hashcat -m 10400 hash.txt wordlist.txt
```

### PDF 1.4-1.6 (RC4-128)
```bash
./pdf2hashcat.sh document.pdf > hash.txt
hashcat -m 10500 hash.txt wordlist.txt
```

### PDF 1.4-1.6 (AES-128)
```bash
./pdf2hashcat.sh document.pdf > hash.txt
hashcat -m 25400 hash.txt wordlist.txt
```

### PDF 1.7+ (AES-256)
```bash
./pdf2hashcat.sh document.pdf > hash.txt
hashcat -m 10600 hash.txt wordlist.txt
```

## Hashcat Mode Reference

| Mode  | Description |
|-------|-------------|
| 10400 | PDF 1.1-1.3 (Acrobat 2-4), RC4-40 |
| 10500 | PDF 1.4-1.6 (Acrobat 5-8), RC4-128 |
| 10600 | PDF 1.7 Level 3-8 (Acrobat 9+), AES-256 |
| 10700 | PDF 1.4-1.6 (Acrobat 5-8), RC4-128 (user password) |
| 25400 | PDF 1.4-1.6 (Acrobat 5-8), AES-128 |

## How It Works

The script:

1. **Parses PDF structure** - Reads the PDF file and locates the encryption dictionary
2. **Extracts encryption parameters** - Gets version (V), revision (R), permissions (P), and encryption strings (O, U, OE, UE, Perms)
3. **Retrieves document ID** - Extracts the unique document identifier from the PDF trailer
4. **Formats for hashcat** - Creates properly formatted hash string based on encryption type

## Example Output

```
$pdf$4*4*128*-1028*1*16*a1b2c3d4e5f6g7h8*32*u9i8o7p6q5w4e3r2t1y0*48*o0p9i8u7y6t5r4e3w2q1
```

## Troubleshooting

### "Not a valid PDF file"
- Ensure the file is actually a PDF
- Check if the file is corrupted

### "No encryption found"
- The PDF may not be password-protected
- The PDF might use a newer unsupported encryption method

### "Could not extract encryption parameters"
- The PDF structure may be malformed
- Try the `-v` flag to see what parameters were found

## Supported Encryption Types

The script handles all standard PDF encryption specifications:

- **Standard Security Handler (Revision 2)** - 40-bit RC4
- **Standard Security Handler (Revision 3)** - 128-bit RC4
- **Standard Security Handler (Revision 4)** - 128-bit AES
- **Standard Security Handler (Revision 5)** - 256-bit AES (Extension Level 3)
- **Standard Security Handler (Revision 6)** - 256-bit AES (Extension Level 8)

## Legal Notice

This tool is intended for:
- Password recovery of your own documents
- Authorized security testing and penetration testing
- Educational purposes and security research
- CTF competitions and challenges

**Only use this tool on PDFs you own or have explicit written permission to test.**

## Technical Details

### PDF Encryption Structure

The script extracts these key components from the PDF:

- **V** - Encryption algorithm version
- **R** - Standard security handler revision
- **P** - Permission flags
- **O** - Owner password hash
- **U** - User password hash
- **OE** - Owner encryption key (R5/6 only)
- **UE** - User encryption key (R5/6 only)
- **Perms** - Encrypted permissions (R5/6 only)
- **ID** - Document identifier from trailer

### Hash Format

The output follows hashcat's expected format:

```
$pdf$V*R*keylen*P*EncryptMetadata*id_len*id*u_len*u*o_len*o[*oe_len*oe*ue_len*ue*perms_len*perms]
```

Where bracketed fields are only present for PDF 1.7+ (R5/6).

## Why Bash?

- Available by default on virtually all Unix/Linux systems
- No additional languages required (Python, Perl, Ruby, etc.)
- Uses only standard Unix tools (grep, awk, xxd, tr)
- Lightweight and fast
- Easy to read and modify
- Cross-platform compatible
- Perfect for quick security assessments

## Contributing

This tool is part of a security research project. Contributions welcome for:
- Supporting additional PDF encryption methods
- Performance improvements
- Better error handling
- Additional output formats

## License

Use responsibly and ethically. This tool should only be used for legitimate security testing purposes.
