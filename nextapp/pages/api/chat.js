export default async function (req, res) {
  const response = await fetch(process.env.LCC_ENDPOINT_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",      
    },
    body: JSON.stringify({
      question: req.body.message,
      session_id: "1234", 
    }),
  });

  const data = await response.json();
  console.log(data); // Logging the response

  res.status(200).json({ result: data });
}
